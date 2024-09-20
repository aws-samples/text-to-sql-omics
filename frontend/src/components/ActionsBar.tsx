import {
  Copy,
  CopySimple,
  FileX,
  Folder,
  TerminalWindow,
  ThumbsDown,
  ThumbsUp,
} from '@phosphor-icons/react';
import MiniButton from './MiniButton';
import { useAtom } from 'jotai';
import { queryStepAtom } from '../atoms';

interface ActionsBarProps {
  data: string | React.ReactNode;
  size?: 'sm' | 'lg';
  onSave?: any;
  onThumbsUp?: any;
  onThumbsDown?: any;
  onCopy?: any;
  onSQL?: any;
}
function ActionsBar(props: ActionsBarProps) {
  const [queryStep] = useAtom(queryStepAtom);

  return (
    <>
      {queryStep == 'loaded' && (
        <>
          {props.size == 'sm' && (
            <div>
              <MiniButton onClick={props.onCopy} title='Copy'>
                <CopySimple size={15} weight='bold'></CopySimple>
              </MiniButton>
              <MiniButton onClick={props.onThumbsDown} title='Thumbs Up'>
                <ThumbsUp size={15} weight='bold'></ThumbsUp>
              </MiniButton>
              <MiniButton onClick={props.onThumbsUp} title='Thumbs Down'>
                <ThumbsDown size={15} weight='bold'></ThumbsDown>
              </MiniButton>
            </div>
          )}
          {props.size != 'sm' && (
            <div className='flex items-center mt-2  justify-end'>
              <MiniButton label='Save' onClick={props.onSave}>
                <Folder weight='bold'></Folder>
              </MiniButton>
              <MiniButton label='Copy' onClick={props.onCopy}>
                <Copy weight='regular'></Copy>
              </MiniButton>
              <MiniButton label='Export'>
                <FileX weight='regular'></FileX>
              </MiniButton>
              <MiniButton label='View SQL' onClick={props.onSQL}>
                <TerminalWindow weight='regular'></TerminalWindow>
              </MiniButton>
            </div>
          )}
        </>
      )}
    </>
  );
}
export default ActionsBar;
