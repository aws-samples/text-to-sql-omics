import Message from './Message';
import Table from './Table';

import { useEffect, useState } from 'react';
import { useAtom } from 'jotai';
import { chatWaitingAtom, convoAtom, queryStepAtom } from '../atoms';
import ChatRefine from '../components/ChatRefine';
import { scrollToBottom } from '../utilities';
import Status from './Status';
import { ResponseDetails } from './ResponseDetails';
function ChatOutput() {
  const [convo] = useAtom(convoAtom);
  const [queryStep] = useAtom(queryStepAtom);
  const [chatWaiting, setChatWaiting] = useAtom(chatWaitingAtom);
  const [waitMessage, setWaitMessage] = useState('');
  const [str] = useState('');
  const [timeouts, setTimeouts] = useState<number[]>([]);

  useEffect(() => {
    if (chatWaiting) {
      const timeout1 = setTimeout(function () {
        setWaitMessage('Please wait');
      }, 5000) as unknown as number;
      const timeout2 = setTimeout(function () {
        setWaitMessage('Just a bit longer');
      }, 10000) as unknown as number;
      const timeout3 = setTimeout(function () {
        setWaitMessage('Still thinking');
      }, 15000) as unknown as number;

      setTimeouts([timeout1, timeout2, timeout3]);
    } else {
      setWaitMessage('');
      timeouts.forEach(clearTimeout);
    }

    return () => timeouts.forEach(clearTimeout);
  }, [chatWaiting, convo]);

  useEffect(() => {
    if (convo[0]?.value) {
      setTimeout(function () {
        scrollToBottom(1000);
      }, 500);
    }
    if (convo[convo.length - 1]?.type == 'Bot') {
      setChatWaiting(false);
    }
  }, [convo]);

  function isText(v: string) {
    let lines = v.split('\n');
    lines = lines.splice(0, 2); //check first 2 lines of results
    const numCommas = lines[0].split(',').length - 1;
    if (lines.length == 2 && numCommas >= 1) {
      return false;
    }else if (lines.length <= 1 || numCommas == 0) {
      return true;
    }
    for (let i = 1; i < lines.length; i++) {
      let tempLine = lines[i];
      tempLine = tempLine.replace(/\".+\"/g, '""'); //ignore commas inside quotes
      const currentLineCommas = tempLine.split(',').length - 1;
      if (currentLineCommas !== numCommas) {
        return true;
      }
    }
    return false;
  }

  return (
    <>
      {convo.length > 0 && (
        <section className='mb-16 gap-10 -mt-10 flex-col flex'>
          {convo.map((o, i) => {
            return (
              <div key={i}>
                {i >= 1 && (
                  <div className='leading-6'>
                    {isText(o.value) ? (
                      <>
                        <Message
                          type={o.type}
                          animate={
                            (new Date().getTime() -
                              new Date(o.date).getTime()) /
                              1000 <
                            20
                              ? true
                              : false
                          }
                        >
                          {o.value}
                        </Message>
                        {o.type == 'Bot' && (
                          <ResponseDetails
                            genes={o.genesfound}
                            variants={o.variantsFound}
                            timing={o.timing}
                            full_answer={o.full_answer}
                            sql={o.sql}
                            type={o.type}
                            question={o.question}
                            value={o.value}
                          ></ResponseDetails>
                        )}
                      </>
                    ) : (
                      <>
                        <Table sql={o.sql}>{o.value}</Table>
                        <ResponseDetails
                          genes={o.genesfound}
                          variants={o.variantsFound}
                          timing={o.timing}
                          full_answer={o.full_answer}
                          sql={o.sql}
                          type={o.type}
                          question={o.question}
                          value={o.value}
                        ></ResponseDetails>
                      </>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </section>
      )}
      {queryStep == 'loading' && <Status />}

      {chatWaiting && (
        <div className='flex -mt-10 mb-10'>
          <div className='loading_dots mr-3'>
            <span>.</span>
            <span>.</span>
            <span>.</span>
            <span>.</span>
          </div>
          <span className='text-slate-400 text-sm pt-1'>{waitMessage}</span>
        </div>
      )}

      {queryStep == 'loaded' && <ChatRefine />}

      <style>{`
      .loading_dots {
        font-size: 1.5rem;
      }
      .loading_dots span {
        animation: bounce 1s infinite;
        display: inline-block;
        user-select: none;
      }
      .loading_dots span:nth-child(2) {
        animation-delay: 0.2s;
      }
      .loading_dots span:nth-child(3) {
        animation-delay: 0.3s;
      }
      .loading_dots span:nth-child(4) {
        animation-delay: 0.4s;
      }


      `}</style>
      {str.length > 0 && <Table>{str}</Table>}
    </>
  );
}

export default ChatOutput;
