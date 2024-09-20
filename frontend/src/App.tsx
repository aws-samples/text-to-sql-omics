import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import ChatIntro from './components/ChatIntro';
import ChatStart from './components/ChatStart';
import ChatOutput from './components/ChatOutput';
import History from './components/History';
import Navigation from './components/Navigation';
import { useAtom } from 'jotai';
import { convoAtom, MessageType, queryStepAtom } from './atoms';
import { getSession } from './graphql/queries';
import * as subscriptions from './graphql/subscriptions';
import Error from './pages/Error';

import { withAuthenticator } from '@aws-amplify/ui-react';

import { generateClient } from 'aws-amplify/api';
const client = generateClient();

function App() {
  let params = useParams<{ sessionId?: string }>();
  const [showError, setShowError] = useState(false);
  const [, setConvo] = useAtom(convoAtom);
  const [, setQueryStep] = useAtom(queryStepAtom);

  async function loadChat() {
    console.log('Loading session: ' + params.sessionId);
    let res: any = await client.graphql({
      query: getSession,
      variables: {
        id: params.sessionId ?? '',
      },
    });
    if (!res.data.getSession) {
      setShowError(true);
    } else {
      setShowError(false);
    }

    let resMessages: string[] = res.data?.getSession?.messages ?? [];

    const conversation: MessageType[] = resMessages.map((chat: string) =>
      JSON.parse(chat)
    );
    console.log(conversation);
    if (conversation.length > 1) {
      setQueryStep('loaded');
      setConvo(conversation);
    }
  }

  function subscribe() {
    return client
      .graphql({
        query: subscriptions.onUpdateSession,
        variables: {
          filter: {
            id: { eq: params.sessionId },
          },
        },
      })
      .subscribe({
        next: (e) => {
          console.log('Subscription Update', e);
          if (e.data.onUpdateSession.id == params.sessionId) {
            setQueryStep('loaded');
            let returnedMessages = e.data.onUpdateSession?.messages?.map(
              (obj) => (obj ? JSON.parse(obj) : null)
            );
            setConvo(returnedMessages ? returnedMessages : []);
          } else {
          }
        },
        error: (error) => console.warn(error),
      });
  }

  useEffect(() => {
    if (params.sessionId) {
      loadChat();
      let subscription = subscribe();
      return () => {
        subscription.unsubscribe();
      };
    } else {
      //askModel('BRCA1');
      setShowError(false);
      setQueryStep('initial');
      setConvo([]);
    }
  }, [params.sessionId]);

  return (
    <>
      <main className='pt-20 mx-auto max-w-6xl xl:w-10/12 md:w-10/12 px-10 lg:px-20 relative text-sm'>
        {showError ? (
          <Error />
        ) : (
          <>
            <ChatIntro />
            <ChatStart />
            <History />
            <ChatOutput />
          </>
        )}
      </main>
      <Navigation />
    </>
  );
}

export default withAuthenticator(App);
