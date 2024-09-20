import MiniButton from './MiniButton';
import { FolderSimple, PlusSquare, SignOut } from '@phosphor-icons/react';
import { useEffect, useRef, useState } from 'react';
import Snippets from '../components/Snippets';
import { useAtom } from 'jotai';
import { SnippetType, snippetsAtom, queryStepAtom } from '../atoms';

import { withAuthenticator } from '@aws-amplify/ui-react';
import type { WithAuthenticatorProps } from '@aws-amplify/ui-react';
import BackToTop from './BackToTop';
import { useNavigate } from 'react-router';
function Navigation({ signOut }: WithAuthenticatorProps) {
  const navigate = useNavigate();
  const [showSnippets, setShowSnippets] = useState(false);
  const [showMenu, setShowMenu] = useState(false);
  const [snippets, setSnippets] = useAtom(snippetsAtom);
  const popupRef = useRef<HTMLDivElement>(null);
  const [, setQueryStep] = useAtom(queryStepAtom);

  useEffect(() => {
    let localSnippets: SnippetType[] = JSON.parse(
      localStorage.getItem('snippets') as string
    );
    if (localSnippets?.length > 0) {
      setSnippets(localSnippets);
    }

    function handleClickOutside(event: MouseEvent) {
      if (
        popupRef.current &&
        !popupRef.current.contains(event.target as Node)
      ) {
        setShowSnippets(false);
        setShowMenu(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <>
      <div ref={popupRef}>
        {showSnippets && <Snippets />}
        {showMenu && (
          <div className='z-50 fadeIn bg-white fixed top-2 right-16 rounded-md shadow-md p-2 gap-2 flex flex-col'>
            <MiniButton onClick={signOut} title='Sign Out'>
              Sign Out
            </MiniButton>
          </div>
        )}
      </div>
      <div className='fixed right-0 lg:right-4 top-4 rounded flex flex-col gap-4 items-center'>
        <MiniButton onClick={() => setShowMenu((b) => !b)}>
          <SignOut size={24} />
        </MiniButton>
        <MiniButton onClick={() => setShowSnippets((b) => !b)} title='Snippets'>
          <span
            className=' absolute text-center text-xs pl-1 w-6 text-black'
            style={{ marginTop: '7px' }}
          >
            {snippets.length === 0 ? '' : snippets.length}
          </span>
          <FolderSimple weight='regular' size={27}></FolderSimple>
        </MiniButton>

        <MiniButton
          title='New Chat'
          onClick={() => {
            setQueryStep('initial');
            navigate('/', {
              replace: true,
              state: { triggerFocus: Date.now() },
            });
          }}
        >
          <PlusSquare weight='light' size={27} />
        </MiniButton>
      </div>
      <BackToTop />
    </>
  );
}
export default withAuthenticator(Navigation);
