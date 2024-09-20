import { Button } from '@cloudscape-design/components';

interface MiniButtonProps {
  children?: string | React.ReactNode;
  label?: string;
  className?: string;
  title?: string;
  onClick?: any;
}

function MiniButton(props: MiniButtonProps) {
  return (
    <div className={'inline ' + props.className} title={props.title}>
      <Button variant='inline-link' onClick={props.onClick}>
        <div className='flex items-center px-2 button'>
          <div className={props.label ? 'mr-1' : ''}>{props.children}</div>
          {props.label}
        </div>
      </Button>
    </div>
  );
}

export default MiniButton;
