import { useEffect, useState } from 'react';
import React from 'react';
import { UserCircle, WarningDiamond } from '@phosphor-icons/react';
import ActionsBar from './ActionsBar';
import { saveMessage } from '../utilities';
import { useParams } from 'react-router';
import javascriptHighlight from '@cloudscape-design/code-view/highlight/javascript';
import { CodeView } from '@cloudscape-design/code-view';

interface MessageProps {
  children: string;
  animate?: boolean;
  type: string;
}

function Message(props: MessageProps) {
  const [showWarning, setShowWarning] = useState(true);
  const params = useParams();
  const animate = props.animate || false;

  useEffect(() => {
    if (typeof props.children === 'string') {
      if (
        (props.children.length > 20 && !props.children.includes(' ')) ||
        props.children.toLowerCase().includes('unable') ||
        props.children.toLowerCase().includes('not found') ||
        props.children.toLowerCase().includes('error')
      )
        setShowWarning(true);
    }
  }, [props.children]);

  async function onCopy() {
    try {
      await navigator.clipboard.writeText(props.children);
      alert('Copied');
    } catch (err) {
      alert('Error' + err);
      console.error('Failed to copy: ', err);
    }
  }
  async function onThumbsDown() {
    if (params.sessionId) {
      await saveMessage(
        'Bot',
        'Thank you for your feedback. Feel free to provide any additional details in the chat below.',
        params.sessionId
      );
    }
  }
  async function onThumbsUp() {
    if (params.sessionId) {
      await saveMessage(
        'Bot',
        'Thank you for your feedback. Feel free to provide any additional details in the chat below.',
        params.sessionId
      );
    }
  }
  return (
    <>
      {props.type == 'Human' && (
        <div className='growIn pl-1 flex items-start xl:w-9/12'>
          <div className='pt-2'>
            <UserCircle size={24}></UserCircle>
          </div>
          <div className='bg-slate-100 rounded-lg ml-2 p-2'>
            {props.children}
          </div>
        </div>
      )}

      {props.type == 'Bot' && (
        <div className='group border-slate-800 xl:w-9/12'>
          <div className='flex items-stretch'>
            <div
              className='-mb-1 w-9 -ml-9 flex items-end justify-center
             opacity-0 rounded-md p-1 mr-2 group-hover:opacity-100 transition-opacity duration-300
             '
            >
              <ActionsBar
                size='sm'
                data={props.children}
                onThumbsUp={onThumbsUp}
                onThumbsDown={onThumbsDown}
                onCopy={onCopy}
              />
            </div>
            {!showWarning && (
              <div className='summon'>
                <TextFormatter animate={animate}>
                  {props.children}
                </TextFormatter>
              </div>
            )}

            {showWarning && (
              <div className='summon'>
                <div className='-ml-1'>
                  <WarningDiamond size={25} color='orange' />
                </div>
                <TextFormatter animate={animate}>
                  {' Oops, there was a problem: ' +
                    props.children.replace(/\n/g, '')}
                </TextFormatter>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}

function TextFormatter(props: { children: string; animate: boolean }) {
  const parts = props.children.split(/(```)/g);
  let isCodeBlock = false;
  const blocks = [];

  for (let i = 0; i < parts.length; i++) {
    // Toggle the isCodeBlock flag when encountering ```
    if (parts[i] === '```') {
      isCodeBlock = !isCodeBlock;
      continue;
    }
    // Depending on the flag, push the appropriate block
    if (isCodeBlock) {
      blocks.push(<CodeBlock key={`code-${i}`}>{parts[i].trim()}</CodeBlock>);
    } else {
      // Avoid pushing empty text blocks
      if (parts[i].trim() !== '') {
        blocks.push(
          <TextBlock animate={props.animate} key={`text-${i}`}>
            {parts[i].trim()}
          </TextBlock>
        );
      }
    }
  }

  return <>{blocks}</>;
}
function CodeBlock(props: { children: string }) {
  return (
    <div className='font-mono my-2 pt-5 bg-slate-100 rounded-lg'>
      <CodeView
        content={props.children}
        highlight={javascriptHighlight}
      ></CodeView>
    </div>
  );
}

function TextBlock(props: { children: string; animate?: boolean }) {
  let wordCounter = 0;
  let txt = props.children.split('\n\n').map((paragraph, paragraphIndex) => {
    let lines = paragraph.split('\n').map((line, lineIndex, array) => (
      <React.Fragment key={'l_' + lineIndex}>
        {line.split(' ').map((word, wordIndex) => {
          wordCounter++;
          return (
            <React.Fragment key={wordIndex}>
              {props.animate ? (
                <span
                  style={{
                    animation: 'summon .5s backwards',
                    animationDelay: wordCounter * 50 + 'ms',
                  }}
                >
                  {word}
                </span>
              ) : (
                <span>{word}</span>
              )}
              {wordIndex < line.split(' ').length - 1 ? ' ' : ''}
            </React.Fragment>
          );
        })}
        {lineIndex < array.length - 1 && <br />}
      </React.Fragment>
    ));
    return <p key={'p_' + paragraphIndex}>{lines}</p>;
  });
  return <div className='space-y-5'>{txt}</div>;
}

export default Message;
