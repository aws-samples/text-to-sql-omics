import { useEffect, useState } from 'react';
import TI from 'react-autocomplete-input';

//@ts-ignore
const TextInput = TI.default ? TI.default : TI;

interface ChatBoxProps {
  placeholder?: string;
  value?: string;
  disabled?: boolean;
  onSubmit: (e: React.FormEvent) => void;
  onChange: (value: string) => void;
}

function ChatBox(props: ChatBoxProps) {
  const [value, setValue] = useState<string>('');

  useEffect(() => {
    if (props.value != undefined) {
      setValue(props.value);
    }
  }, [props.value]);

  let enabledStyle = `w-full rounded-md pt-5 pl-4 text-md border shadow-sm focus:outline focus:outline-violet-400 h-auto resize-y h-[54px]`;
  let disabledStyle = `w-full rounded-md pt-5 pl-4 text-md bg-slate-100/60 backdrop-blur-sm border-b border-slate-300 resize-y h-[54px]`;

  return (
    <>
      <TextInput
        className={!props.disabled ? enabledStyle : disabledStyle}
        placeholder={props.placeholder}
        value={value}
        trigger={[' ']}
        minChars={2}
        disabled={props.disabled}
        onFocus={() => {
          if (!value) {
            setValue(' '); //force a space so autocomplete can trigger
          }
        }}
        onChange={(e: string) => {
          props.onChange(e);
          setValue(e);
        }}
        onKeyDown={(e: React.KeyboardEvent) => {
          if (e.key == 'Enter' && !e.shiftKey) {
            props.onSubmit(e);
          }
        }}
        defaultValue={props.value}
      />
    </>
  );
}
export default ChatBox;
