import { parse } from 'papaparse';
import { useEffect, useRef, useState } from 'react';
import { useParams } from 'react-router';
import {
  Table as CloudscapeTable,
  TextFilter,
} from '@cloudscape-design/components';
import ActionsBar from './ActionsBar';
import html2canvas from 'html2canvas';
import { useAtom } from 'jotai';
import { SnippetType, snippetsAtom } from '../atoms';
import javascriptHighlight from '@cloudscape-design/code-view/highlight/javascript';
import { CodeView } from '@cloudscape-design/code-view';
interface TableProps {
  children: string | React.ReactNode;
  sql?: string | null;
  hideActions?: boolean;
}

function Table(props: TableProps) {
  const params = useParams();
  /* let propschildren =
    ',City,Dogs,Cats,Other Pets\r\nVisited,Jacksonville, 1,2,5\r\nTransported,Raleigh,3,5,8\r\n';
   */

  const [csv] = useState(props.children);
  const [myDefinitions, setMyDefinitions] = useState([]);
  const [myArray, setMyArray] = useState([]);
  const [totalResults, setTotalResults] = useState();
  const [snippets, setSnippets] = useAtom(snippetsAtom);
  const [showSQL, setShowSQL] = useState(false);
  const tableElement = useRef(null);
  const rowLimit = 20;

  async function onCopy() {
    try {
      await navigator.clipboard.writeText(props.children);
      alert('Copied');
    } catch (err) {
      alert('Error' + err);
      console.error('Failed to copy: ', err);
    }
  }

  function onSQL() {
    setShowSQL((b) => !b);
  }

  function screenshot() {
    let table = tableElement.current;
    html2canvas(table).then((canvas) => {
      const canvasImg = canvas.toDataURL('image/png');
      // Create an image element to display the screenshot
      let imgElement = document.createElement('img');
      imgElement.src = canvasImg;
      imgElement.classList.add('screenshot');
      document.body.appendChild(imgElement);
      let sn: SnippetType = {
        title: 'Snippet ' + (snippets.length + 1),
        parentId: params.sessionId || '',
        date: new Date().toISOString(),
        data: props.children,
        img: canvasImg,
      };
      setSnippets((o) => [...o, sn]);
    });
  }

  useEffect(() => {
    if (snippets.length > 0) {
      localStorage.setItem('snippets', JSON.stringify(snippets));
    }
  }, [snippets]);

  useEffect(() => {
    if (csv) {
      const parsedData = parse(csv, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        transformHeader: (header) => header.toLowerCase().replace(/ /g, '_'),
      }).data;
      setTotalResults(parsedData.length);

      const parsedDataExcerpt = parsedData.splice(0, rowLimit);

      const content = parsedDataExcerpt.map((item) => {
        const newItem = {};
        for (const [key, value] of Object.entries(item)) {
          newItem[key] = value;
        }
        return newItem;
      });

      const headers = csv.substring(0, csv.indexOf('\n')).split(',');

      let definitions = headers.map((header, index) => {
        const id = header.toLowerCase().replace(/ /g, '_');
        header = header.replace(/_/g, ' ').toUpperCase();
        return {
          id,
          header,
          cell: (e) => e[id],
          ...(index === 0 ? { isRowHeader: true } : {}), // Mark the first column as the row header
        };
      });
      setMyArray(content);
      console.log(definitions);
      setMyDefinitions(definitions);
    } else {
      console.log('not csv', props.children);
    }
  }, []);
  return (
    <>
      <div className='flex group'>
        <div
          className='-mb-1 w-9 -ml-9 flex items-end justify-center
             opacity-0 rounded-md p-1 mr-2 group-hover:opacity-100 transition-opacity duration-300
             '
        >
          <ActionsBar
            data={props.children}
            onSave={screenshot}
            onCopy={onCopy}
            size='sm'
          />
        </div>
        <div
          className='p-3 border rounded-md bg-white relative w-full'
          ref={tableElement}
        >
          <div className='py-8 absolute right-2 z-10 -mt-8'></div>
          {myDefinitions.length >= 1 && (
            <CloudscapeTable
              variant='borderless'
              columnDefinitions={myDefinitions}
              items={myArray}
              sortingColumn='Air'
              footer={
                <span>    {totalResults} rows found.{' '}
                {totalResults !== undefined &&
                  totalResults >= rowLimit &&
                  `Showing 1-${rowLimit}.`}
                </span>
              }
            />
          )}
        </div>

        <style>{`
      thead {
        box-shadow: 0px 1px 0px 0px #aaa;
      }
`}</style>
      </div>
      {!props.hideActions && (
        <ActionsBar
          data={props.children}
          onSave={screenshot}
          onCopy={onCopy}
          onSQL={onSQL}
        />
      )}
      {showSQL && (
        <div className='rounded-md right-0 ml-auto text-white w-full text-sm fadeIn mb-8'>
          <CodeView
            content={props.sql ? props.sql : 'Unknown'}
            highlight={javascriptHighlight}
          ></CodeView>
        </div>
      )}
    </>
  );
}
export default Table;
