import { useEffect, useState } from 'react';
import { useParams } from 'react-router';
import { MessageType, convoAtom } from '../atoms';
import { useAtom } from 'jotai';
import { askModel } from '../utilities';

function Samples(props: any) {
  const params = useParams();
  const [convo] = useAtom<MessageType[]>(convoAtom);

  const [txt, setTxt] = useState<string[]>([]);

  function selectSample(z: string) {
    props.handleSelect(z);
  }

  useEffect(() => {
    if (params.sessionId) {
      /* setTxt([
        'Show me more...',
        'What kinds of predicted loss-of-function variants are here?',
        'Please include annotations',
        'Is this likely pathogenic?',
        'Only show from East asian ancestries',
      ]); */
      //ID exists, show refinement examples
    } else {
      setTxt([
        'Summarize pathogenic variants in LDLR',
        'frequency of variant 17:7041768:G:T',
        'deletions in exon 5 of TP53',
        'what proportion of pLOFs are singletons in gene CHCHD2P8?',
      ]);
    }
  }, [params.sessionId]);

  async function getSampleFeedbackResponses() {
    let txt = await askModel(
      `Generate a javascript array consisting of 6 strings in sentence case.
      Do not create full sentences. Each string should be a fragment or a phrase
      a user may tell a chatbot after giving it a thumbs down. The chatbot has asked for clarification.`
    );
    let txtarr = txt.split('= ')[1].split(']')[0] + ']';
    let arr = JSON.parse(txtarr);
    setTxt(arr);
    return txt;
  }

  async function getSampleRefinements() {
    let entireChat = '';
    entireChat = convo
      .map((d) => entireChat + d.type + ': ' + d.value)
      .join(' ');

    let txt = await askModel(
      `Generate a javascript array consisting of 6 strings in sentence case.
      Each string should be a short sentence fragment or short phrases a user may tell a chatbot to further this conversation or dive deeper into the materials.
      Strings should use pronouns instead of the proper nouns if there is a sole primary subject of the conversation. Avoid formal sentences.
      Here is the conversation:
      ${JSON.stringify(entireChat)}
      The Javascript array: `
    );
    let txtarr = txt.split('[')[1].split(']')[0];
    let arr = JSON.parse('[' + txtarr + ']');
    setTxt(arr);
    return txt;
  }

  useEffect(() => {
    if (
      convo.length &&
      convo[convo.length - 1].value.includes('Thank you for your feedback')
    ) {
      getSampleFeedbackResponses();
      /*
      setTxt([
        'Refused to respond',
        '😡',
        'Information is inaccurate',
        'Misunderstanding',
        'Ignored part of my request',
      ]); */
    } else if (convo.length && convo[convo.length - 1].type == 'Bot') {
      getSampleRefinements();
    }
  }, [convo]);
  return (
    <div className='flex items-center mt-2 max-w-6/12 pb-2 overflow-auto'>
      {/*       <small className='cursor-pointer' title='More' onClick={() => shuffle()}>
        <DotsThreeCircle weight='light' size={29} />
      </small>
 */}{' '}
      {txt.map((t, i) => {
        return (
          <div
            onClick={() => {
              selectSample(t);
            }}
            key={i}
            title='Try this query'
            className='mr-2'
          >
            <Chip>{t}</Chip>
          </div>
        );
      })}
      <style>{`

      div::-webkit-scrollbar {
        width: 5px; /* or any small width */
        height: 2px;
        opacity: 0.25;
      }

      div::-webkit-scrollbar-track {
        background: #f1f1f1; /* Track background */
      }

      div::-webkit-scrollbar-thumb {
        background: #ffffff;
      }
      div:hover::-webkit-scrollbar-thumb {
        background: #88888855; /* Handle color */
      }

      div::-webkit-scrollbar-thumb:hover {
        background: #555;
      }

      `}</style>
    </div>
  );
}

function Chip(props: { children: string }) {
  return (
    <div className='cursor-pointer text-nowrap transition-all hover:border-violet-400 transition-all inline-block rounded-md text-sm border border-slate-300 px-2 py-1 rounded-xl'>
      {props.children}
    </div>
  );
}

export default Samples;
