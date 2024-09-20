import { useEffect } from 'react';
import { useAtom } from 'jotai';
import { convoAtom, queryStepAtom } from '../atoms';

function ChatIntro() {
  const [convo] = useAtom(convoAtom);
  const [queryStep] = useAtom(queryStepAtom);
  useEffect(() => {}, [convo]);

  return (
    <section
      className={queryStep === 'initial' ? 'collapsible' : 'collapsible hidden'}
    >
      <div>
        <h2 className="font-bold text-2xl">Explore the Dataset.</h2>
        <p className="lg:w-7/12 my-6">
          Welcome to the dataset. I can help find the data you need. What would
          you like to see today?
        </p>
      </div>
      <style>{`
.intro-enter {
  opacity: 0;
}
.intro-enter-active {
  opacity: 1;
  transition: opacity 3500ms ease-in;
}
.intro-exit {
  opacity: 1;
}
.intro-exit-active {
  opacity: 0;
  transition: opacity 3500ms ease-in;
}`}</style>
    </section>
  );
}
export default ChatIntro;
