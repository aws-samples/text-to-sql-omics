import { useEffect, useState } from 'react';
import { useAtom } from 'jotai';
import { SnippetType, snippetsAtom } from '../atoms';

import TimeAgo from 'timeago-react';
import { X } from '@phosphor-icons/react';
import Table from './Table';
import MiniButton from './MiniButton';

function Snippets() {
  const [snippets, setSnippets] = useAtom(snippetsAtom);
  const [showDetails, setShowDetails] = useState(false);
  const [activeSnippet, setActiveSnippet] = useState(0);
  useEffect(() => {
    let storedItem = localStorage.getItem('snippets');
    let s: SnippetType[] =
      storedItem !== null ? (JSON.parse(storedItem) as SnippetType[]) : [];
    if (s?.length > 0) {
      setSnippets(s);
    }
  }, []);
  function viewDetails(i: number) {
    setShowDetails(true);
    setActiveSnippet(i);
    console.log(i);
  }
  return (
    <>
      {snippets.length > 0 ? (
        <div className='z-50 fadeIn bg-white fixed w-128 top-16 right-16 rounded-md shadow-md overflow-auto max-h-96'>
          <h3 className='font-bold p-3 sticky top-0 bg-white border-b'>
            Snippets ({snippets.length})
          </h3>
          {snippets.map((s, i) => {
            return (
              <div
                key={i}
                className='border-b p-3 flex hover:bg-slate-100 max-w-md cursor-pointer'
                onClick={() => viewDetails(i)}
              >
                <div className='flex'>
                  <div className='border shadow mr-4 w-3/12 bg-white'>
                    <img src={s.img} />
                  </div>
                  <div className='text-nowrap w-9/12'>
                    <h6>{s.title}</h6>
                    <small className='text-slate-400'>
                      <TimeAgo datetime={s.date} />
                    </small>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className='z-50 fadeIn bg-white fixed w-74 top-16 right-16 rounded-md shadow-md border'>
          <div className='p-0 py-6 text-center'>
            <h3 className='font-bold'>You haven&rsquo;t saved any snippets.</h3>

            <img src='save_example.png' className='w-full my-4' />

            <small>
              Click <strong>Save</strong> on any data table to use snippets.
            </small>
          </div>
        </div>
      )}
      {showDetails && (
        <div className='fixed w-full h-full flex p-4 z-50 backdrop-brightness-90 backdrop-blur-md top-0 gap-2 fadeIn'>
          <div className='bg-white shadow-lg rounded-lg w-full mx-auto p-12 overflow-auto'>
            <div className='mb-12 flex items-start justify-between'>
              <h2 className='text-xl'> {snippets[activeSnippet].title}</h2>

              <div className='flex'>
                <MiniButton label='Rename'></MiniButton>
                <MiniButton label='Delete'></MiniButton>
              </div>
            </div>
            <Table hideActions={true}>{snippets[activeSnippet].data}</Table>
          </div>
          <button
            className='bg-white rounded-full h-auto p-2 self-start hover:text-violet-700 shadow'
            onClick={() => setShowDetails(false)}
          >
            <X size={28}></X>
          </button>
        </div>
      )}
    </>
  );
}

export default Snippets;
