import TI from 'react-autocomplete-input';
import { Button } from '@cloudscape-design/components';
import React, { useEffect, useState } from 'react';
import { Link, useLocation, useParams } from 'react-router-dom';
import Samples from './Samples';
import 'react-autocomplete-input/dist/bundle.css';
import {
  askModel,
  createNewSession,
  saveMessage,
  loadSession,
} from '../utilities';
import { useNavigate } from 'react-router-dom';
import { useAtom } from 'jotai';
import { queryStepAtom } from '../atoms';
import { ArrowLeft, PaperPlaneRight } from '@phosphor-icons/react';
import { convoAtom } from '../atoms';
import ChatBox from './ChatBox';
import { useRef } from 'react';

//@ts-ignore
const TextInput = TI.default ? TI.default : TI;

function ChatStart() {
  const [queryStep, setQueryStep] = useAtom(queryStepAtom);
  const [value, setValue] = useState<string>('');
  const location = useLocation();
  const navigate = useNavigate();
  const [convo] = useAtom(convoAtom);
  const params = useParams();

  let startInput = useRef<HTMLFormElement>(null);

  const handleChange = (newValue: string) => {
    setValue(newValue);
  };

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (value.trim().length) {
      let sessionId = await createNewSession();

      //save to dynamoDB
      await saveMessage('Human', value, sessionId);
      setQueryStep('loading');
      let s = await loadSession(sessionId);
      navigate('/' + sessionId);
      setValue(s.title);

      //send to Model
      try {
        await askModel(value, sessionId);
        setQueryStep('loaded');
      } catch (e) {
        console.log('Timed out. Still subscribed though, stay tuned.');
      }
    }
  }

  function onSelect(e: string) {
    console.log(e);
    setValue(e);
  }

  useEffect(() => {
    if (convo[0]?.value.length > 0) {
      setValue(convo[0].value);
    } else {
      if (!params.sessionId && startInput.current != null) {
        (startInput.current.childNodes[0] as HTMLFormElement).focus();
        setValue(' ');
      }
    }
  }, [convo, location.key]);

  return (
    <>
      <div
        className={
          queryStep == 'initial'
            ? 'revise_query sticky top-8 -ml-9 lg:-ml-12 duration-500 h-0 transition-all z-10'
            : 'revise_query sticky top-8 -ml-9 lg:-ml-12 duration-500 h-14 transition-all z-10'
        }
      >
        {queryStep != 'initial' && (
          <>
            {' '}
            <Link to='/' onClick={() => setValue('')}>
              <Button variant='inline-link'>
                <div className='flex items-center button'>
                  <ArrowLeft size={30}></ArrowLeft>
                </div>
              </Button>
            </Link>
          </>
        )}
      </div>
      <section
        className={
          queryStep == 'loaded'
            ? 'sticky top-2 pt-3 z-30 text-lg '
            : 'top-2 pt-3 text-lg'
        }
      >
        <div className='flex sticky'>
          <form
            className='w-full flex'
            onSubmit={handleSubmit}
            ref={startInput}
          >
            <ChatBox
              placeholder='Enter a query with an gene, variant name, or Rsid'
              value={value}
              onChange={handleChange}
              onSubmit={handleSubmit}
              disabled={queryStep != 'initial' ?? true}
            ></ChatBox>
            {queryStep == 'initial' && (
              <>
                {value.trim().length > 0 ? (
                  <button className='bg-violet-700 rounded-md ml-1 flex items-center p-3 text-white hover:text-white hover:bg-slate-800 transition-all duration-200 shadow active:translate-y-0.5'>
                    <PaperPlaneRight size={20}></PaperPlaneRight>
                  </button>
                ) : (
                  <button
                    disabled
                    className='bg-slate-200 rounded-md ml-1 flex items-center p-3 text-slate-400 '
                  >
                    <PaperPlaneRight size={20}></PaperPlaneRight>
                  </button>
                )}
              </>
            )}
          </form>
        </div>
        {queryStep == 'initial' && (
          <div className='flex justify-between mt-0'>
            <Samples
              handleSelect={(m: string) => {
                onSelect(m);
              }}
            />
          </div>
        )}
      </section>
      <style>{`

.revise_query {
  animation: fadeIn 0.8s;
}

`}</style>
    </>
  );
}

export default ChatStart;
