import { useState, useEffect } from 'react';

function Status() {
  const [visibleTag, setVisibleTag] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setVisibleTag((prev) => prev + 1);
    }, visibleTag * 3500);
    return () => clearInterval(interval);
  }, [visibleTag]);
  return (
    <div className='h-48'>
      <div className='-mb-16'>
        <img src='loader.svg' className='animate-bounce mx-auto w-12' />
      </div>

      <div className='mt-24 text-center gap-2 flex flex-col'>
        {visibleTag >= 2 && (
          <p className={visibleTag === 2 ? 'animate-pulse' : ''}>
            Analyzing request
          </p>
        )}
        {visibleTag >= 3 && (
          <p className={visibleTag === 3 ? 'animate-pulse delay-100' : ''}>
            Identifying genes
          </p>
        )}
        {visibleTag >= 4 && (
          <p className={visibleTag === 4 ? 'animate-pulse delay-300' : ''}>
            Querying data
          </p>
        )}
        {visibleTag >= 5 && (
          <p className={visibleTag === 5 ? 'animate-pulse delay-300' : ''}>
            Generating response
          </p>
        )}
      </div>
    </div>
  );
}

export default Status;
