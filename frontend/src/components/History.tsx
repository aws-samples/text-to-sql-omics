import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import TimeAgo from 'timeago-react';
import { ClockCounterClockwise, X } from '@phosphor-icons/react';
import { useAtom } from 'jotai';
import { queryStepAtom } from '../atoms';
import MiniButton from './MiniButton';
import { fetchAuthSession } from 'aws-amplify/auth';
import { sessionsByDate } from '../graphql/queries';
import * as subscriptions from '../graphql/subscriptions';
import { generateClient } from 'aws-amplify/api';
import { deleteSession } from '../graphql/mutations';
const client = generateClient();

interface Session {
  id: string;
  createdAt: string;
  title?: string;
}

function History() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [queryStep] = useAtom(queryStepAtom);

  async function loadSessions() {
    await fetchAuthSession();
    let res: any = await client.graphql({
      query: sessionsByDate,
      variables: {
        type: 'Session',
      },
    });
    setSessions(res.data.sessionsByDate.items.reverse());
  }

  function createSubscriptions() {
    console.log('Subscribed to sessions.');
    client.graphql({ query: subscriptions.onDeleteSession }).subscribe({
      next: (e) => {
        console.log('Deleted', e.data.onDeleteSession.id);
        setSessions((sess) =>
          sess.filter((item) => item.id !== e.data.onDeleteSession.id)
        );
      },
    });
    client.graphql({ query: subscriptions.onCreateSession }).subscribe({
      next: (e) => {
        setSessions((s) => [e.data.onCreateSession as Session, ...s]);
      },
    });

    loadSessions();
  }

  useEffect(() => {
    createSubscriptions();
  }, []);

  async function deleteChat(id: string) {
    await client.graphql({
      query: deleteSession,
      variables: {
        input: {
          id: id,
        },
      },
    });

    loadSessions();
  }

  return (
    <section
      className={
        queryStep === 'initial'
          ? 'collapsible lg:w-10/12 mt-12'
          : 'collapsible lg:w-10/12 mt-12 hidden'
      }
    >
      {sessions.length > 0 && (
        <div>
          <h6 className='font-bold text-sm mb-6'>
            <div className='flex items-center'>
              <ClockCounterClockwise weight='bold'></ClockCounterClockwise>
              <span className='ml-2'>My History</span>
            </div>
          </h6>
          {sessions.map((s, i) => {
            return (
              <div key={i} className='transition-all duration-300'>
                <div className='flex text-sm justify-between hover:bg-slate-100 ml-4 rounded'>
                  <div className='flex w-full items-center'>
                    <MiniButton onClick={() => deleteChat(s.id)}>
                      <div className='hover:bg-violet-600 hover:text-white rounded active:bg-violet-700 p-1'>
                        <X></X>
                      </div>
                    </MiniButton>
                    <Link
                      className='p-3 pl-0 flex flex-grow justify-between'
                      to={'/' + s.id}
                    >
                      {s.title}
                      <small className='text-nowrap'>
                        <TimeAgo
                          datetime={new Date(s.createdAt).toISOString()}
                        />
                      </small>
                    </Link>
                  </div>
                </div>
              </div>
            );
          })}{' '}
        </div>
      )}
    </section>
  );
}

export default History;
