import MiniButton from './MiniButton';
import { CaretDoubleUp } from '@phosphor-icons/react';
import { scrollToTop } from '../utilities';
import { useEffect, useState } from 'react';

function BackToTop() {
  const [showButton, setShowButton] = useState(false);
  useEffect(() => {
    const handleScroll = () => {
      const totalHeight =
        document.documentElement.scrollHeight - window.innerHeight;
      // Calculate the current scroll position as a percentage of the total height
      const scrollPosition = (window.scrollY / totalHeight) * 100;
      const perc = scrollPosition.toFixed(2);
      if (parseInt(perc) > 80) {
        setShowButton(true);
      } else {
        setShowButton(false);
      }
    };

    window.addEventListener('scroll', handleScroll);

    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <>
      {showButton && (
        <div className='fixed bottom-0 pb-4 right-0 lg:right-4 fadeIn pt-2'>
          <MiniButton title='Back to Top' onClick={() => scrollToTop(1000)}>
            <CaretDoubleUp size={20}></CaretDoubleUp>
          </MiniButton>
        </div>
      )}
    </>
  );
}

export default BackToTop;
