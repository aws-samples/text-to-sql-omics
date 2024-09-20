import React, { useState } from 'react';

import { useParams } from 'react-router';
import { askModel, saveMessage } from '../utilities';
import { useAtom } from 'jotai';
import { convoAtom, chatWaitingAtom } from '../atoms';
import Samples from './Samples';
import ChatBox from './ChatBox';
import { PaperPlaneRight } from '@phosphor-icons/react';

function ChatRefine() {
  const params = useParams();
  const [value, setValue] = useState<string>('');
  const [, setChatWaiting] = useAtom(chatWaitingAtom);
  const [convo] = useAtom(convoAtom);

  function onSelect(str: string) {
    setValue(str);
  }

  const handleChange = (newValue: string) => {
    setValue(newValue);
  };

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    let sessionId = params.sessionId || '';
    let messageType: 'Data' | 'Human' = value.includes('\n') ? 'Data' : 'Human';
    //if text multiple lines, consider it data
    setValue('');
    await saveMessage(messageType, value, sessionId);
    if (messageType == 'Human') {
      setChatWaiting(true);
      let entireChat = [];
      entireChat = convo
        .filter((d) => d.type === 'Human')
        .map((d) => d.type + ': ' + d.value.trim());

      entireChat.push('Human: ' + value);

      //      entireChat += value;
      console.log(entireChat);

      //entireChat = entireChat.replace(/\"|\'|\-|\r?\n|\r/g, '');
      let answer = await askModel(entireChat, sessionId);
      await saveMessage('Bot', answer, sessionId);
      setChatWaiting(false);
    }
  }
  return (
    <>
      {convo.length > 1 && (
        <section className='text-lg mb-12'>
          <form className='w-full flex' onSubmit={handleSubmit}>
            <ChatBox
              placeholder='Ask a follow up or refinement query...'
              value={value}
              onChange={handleChange}
              onSubmit={handleSubmit}
            />
            {value.trim().length > 0 ? (
              <button className='bg-violet-700 rounded-md ml-1 flex items-center p-3 text-white hover:text-white hover:bg-slate-800 transition-all duration-200 shadow'>
                <PaperPlaneRight size={20}></PaperPlaneRight>
              </button>
            ) : (
              <button
                disabled
                className='bg-slate-200 rounded-md ml-1 flex items-center p-3 text-slate-400'
              >
                <PaperPlaneRight size={20}></PaperPlaneRight>
              </button>
            )}
          </form>
          <Samples
            handleSelect={(m: string) => {
              onSelect(m);
            }}
          />
        </section>
      )}
    </>
  );
}

export default ChatRefine;
