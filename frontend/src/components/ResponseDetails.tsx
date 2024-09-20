import { CodeView } from '@cloudscape-design/code-view';
import javascriptHighlight from '@cloudscape-design/code-view/highlight/javascript';

interface ResponseDetailsProps {
  children?: string;
  value?: string;
  type?: string;
  question?: string;
  animate?: boolean;
  genes?: string;
  variants?: string;
  timing?: { question_creation?: number; sql_generation?: number };
  full_answer?: string;
  sql?: string | null;
}

export function ResponseDetails(props: ResponseDetailsProps) {
  return (
    <section className="-mt-5">
      <details className="ml-2">
        <summary className="cursor-pointer opacity-40 font-bold text-xs w-14">
          DETAILS
        </summary>
        <div className="p-2 bg-slate-100 pl-3 rounded-lg mt-6">
          <details>
            <summary>
              <span className="font-bold cursor-pointer">Full Query</span>
            </summary>
            <div className="pl-4 text-lg my-2 text-slate-500">
              &ldquo;{props.question}&rdquo;
            </div>
            <div className="pl-4 my-2 overflow-x-auto">
              <pre className="font-sans">{props.full_answer}</pre>
            </div>
          </details>
          <details>
            <summary>
              <span className="font-bold cursor-pointer">Generated SQL</span>
            </summary>
            <CodeView
              content={props.sql ? props.sql : 'No SQL generated'}
              highlight={javascriptHighlight}
            ></CodeView>
          </details>
          <details>
            <summary>
              <span className="font-bold cursor-pointer">Other</span>
            </summary>
            <div className="pl-4">
              <p>
                <span className="font-bold text-slate-500">
                  Processing Time:{' '}
                </span>
                Request Rephrasing:{' '}
                {props.timing?.question_creation?.toFixed(1) + 's'}, SQL
                Generation: {props.timing?.sql_generation?.toFixed(1) + 's'}
              </p>
              <p>
                <span className="font-bold text-slate-500">
                  Genes and Variants:{' '}
                </span>
                {props.genes}, {JSON.stringify(props.variants)}
              </p>
            </div>
          </details>
        </div>
      </details>
    </section>
  );
}
