import { Link, useParams } from 'react-router-dom';
import MiniButton from '../components/MiniButton';
import { ArrowLeft, Warning } from '@phosphor-icons/react';

function Error() {
  const params = useParams();
  return (
    <>
      <div className='-ml-6 mb-12'>
        <Link to='/'>
          <MiniButton label='Back'>
            <ArrowLeft />
          </MiniButton>
        </Link>
      </div>
      <h2 className='font-bold text-2xl flex items-center'>
        <Warning size={24} color='orange' weight='duotone' />
        <span className='ml-2'>Error</span>
      </h2>
      <p className='lg:w-7/12 my-6'>
        There is no session with the name <strong>{params.sessionId}</strong>.
      </p>
    </>
  );
}

export default Error;
