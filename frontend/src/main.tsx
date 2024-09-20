import ReactDOM from 'react-dom/client';
import { Amplify } from 'aws-amplify';
import config from './amplifyconfiguration.json';
import '@aws-amplify/ui-react/styles.css';
import './login.scss';
import './App.css';
import '@cloudscape-design/global-styles/index.css';
import Error from './pages/Error';

import { createBrowserRouter } from 'react-router-dom';
import { RouterProvider } from 'react-router';
import App from './App.tsx';
Amplify.configure(config);

const browserRouter = createBrowserRouter([
  {
    path: 'Error',
    element: <Error />,
  },
  {
    path: '/',
    element: <App />,
    children: [
      { path: ':sessionId', element: <App /> },
      { path: '*', element: <Error /> },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <RouterProvider router={browserRouter} />
);
