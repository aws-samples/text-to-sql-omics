import { atom } from 'jotai';

export interface MessageType {
  value: string;
  type: string;
  date: string;
  question?: string;
  animate?: boolean;
  genesfound?: string;
  variantsFound?: string;
  timing?: { question_creation?: number; sql_generation?: number };
  full_answer?: string;
  sql?: string | null;
}
export interface SnippetType {
  parentId: string;
  date: string;
  data: any;
  img: string;
  title: string;
}
type QueryStepType = 'initial' | 'submitted' | 'loading' | 'loaded';
export const convoAtom = atom<MessageType[]>([]);
export const queryStepAtom = atom<QueryStepType>('initial');
export const chatWaitingAtom = atom<boolean>(false);
export const snippetsAtom = atom<SnippetType[]>([]);
