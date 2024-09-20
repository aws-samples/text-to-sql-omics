import { fetchAuthSession } from 'aws-amplify/auth';
import { v4 as uuidv4 } from 'uuid';
import { createSession, updateSession } from './graphql/mutations';
import { Amplify } from 'aws-amplify';


import {
  BedrockRuntimeClient,
  InvokeModelCommand,
} from '@aws-sdk/client-bedrock-runtime';
import { generateClient } from 'aws-amplify/api';
import { getSession } from './graphql/queries';

export async function createNewSession() {
  let uuid: string = uuidv4();
  let sessionId = makeSlug(uuid);
  return sessionId;
}

export async function askModel(prompt: string | string[], sessionId?: string) {
  if (!prompt || (Array.isArray(prompt) && prompt.length === 0))
    return 'Error: Prompt is empty';
  const input = Array.isArray(prompt) ? prompt : prompt.trim();
  return sessionId
    ? await pingAPI(input, sessionId)
    : await pingBedrock(input as string); //for sample prompts;
}

export async function pingBedrock(prompt: string) {
  let session = await fetchAuthSession();
  if (!prompt) return 'Error: Prompt is empty';

  //format for Bedrock
  let promptBody = `{"prompt":
    ${JSON.stringify('Human: ' + prompt.trim() + ' Assistant:')}
    ,"max_tokens_to_sample":200,"temperature":0.5,"top_k":250,"top_p":1, "stop_sequences":["\\n\\nHuman:"]}`;

  const input = {
    modelId: 'anthropic.claude-instant-v1',
    contentType: 'application/json',
    accept: '*/*',
    body: promptBody,
  };

  let client = new BedrockRuntimeClient({
    region: 'us-east-1',
    credentials: session.credentials,
  });

  if (client) {
    //post to Bedrock
    const command = new InvokeModelCommand(input);
    const response = await client.send(command);
    const decoder = new TextDecoder();
    const text = decoder.decode(response.body);
    let obj = JSON.parse(text);
    return obj.completion ? obj.completion : 'No message has been returned.';
  } else {
    return 'There was an error.';
  }
}

async function pingAPI(input: string | string[], sessionId: string) {
  let session = await fetchAuthSession();

  let query;
  //format input for API
  if (Array.isArray(input)) {
    query = `{"conversation": ${JSON.stringify(
      input
    )},"session_id":"${sessionId}"}`;
  } else {
    query = `{"conversation":["${input}"],"session_id":"${sessionId}"}`;
  }

  //post to API
  let headers = new Headers();
  headers.append('Authorization', `Bearer ${session.tokens?.idToken}`);

  let response = await fetch(import.meta.env.VITE_API_QUERY, {
    method: 'POST',
    headers : headers,
    body: query,
  });

  //handle response
  if (!response.ok) {
    throw new Error('Network response error.');
  }

  let res = await response.json();
  console.log('API response', res);
  return res.rows;
}

export async function saveMessage(
  speaker: 'Human' | 'Data' | 'Bot',
  query: string,
  sessionId: string
) {
  const client = generateClient();

  //get chat session from DynamoDB
  let res: any = await client.graphql({
    query: getSession,
    variables: {
      id: sessionId,
    },
  });

  //reconstruct conversation into JS object
  let convo: any[] = res.data?.getSession?.messages || [];
  convo = convo.map((i) => JSON.parse(i));

  //set to 'create new' if there was no session on Dynamo found
  let queryName = convo.length == 0 ? createSession : updateSession;

  if (query?.trim().length) {
    //push the latest message from UI
    convo?.push({
      value: query,
      type: speaker,
      date: new Date().toISOString(),
    });

    let newObject = {
      id: sessionId,
      type: 'Session',
      title: convo[0].value,
      messages: [...convo].map((msg) => JSON.stringify(msg)),
    };

    //save to DynamoDB
    let allMessages: any = await client.graphql({
      query: queryName,
      variables: {
        input: newObject,
      },
    });

    if (queryName == createSession) {
      return allMessages.data?.createSession?.messages;
    } else {
      return allMessages.data?.updateSession?.messages;
    }
  }
}

export function makeSlug(uuid: string) {
  const consonants = 'bcdfghjklmnpqrstvwxyz';
  const vowels = 'aeiou';
  let customID = '';
  let startWithVowel = Math.floor(Math.random() * 7) === 0;
  const simplifiedUUID = uuid.replace(/-/g, '').substring(0, 30);
  for (let x = 0; x < 15; x++) {
    let i = x;
    const char = simplifiedUUID[i * 2] + simplifiedUUID[i * 2 + 1];
    let base = (x % 2 === 0) !== startWithVowel ? consonants : vowels;
    const index = parseInt(char, 16) % base.length;
    customID += base[index];
  }

  const hyphenatedID = customID.replace(/(.{5})(.{5})/g, '$1-$2-');
  return hyphenatedID || 'undefined';
}

export const scrollToTop = (duration: number) => {
  scrollTo(0, duration);
};
export const scrollToBottom = (duration: number) => {
  scrollTo(document.documentElement.scrollHeight, duration);
};
export const scrollTo = (to: number, duration: number) => {
  const element = document.scrollingElement || document.documentElement;
  const start = element.scrollTop;
  const change = to - start;
  const startDate = +new Date();
  const easeInOutQuad = (t: number, b: number, c: number, d: number) => {
    let t2 = t;
    t2 /= d / 2;
    if (t2 < 1) return (c / 2) * t2 * t2 + b;
    t2 -= 1;
    return (-c / 2) * (t2 * (t2 - 2) - 1) + b;
  };
  const animateScroll = () => {
    const currentDate = +new Date();
    const currentTime = currentDate - startDate;
    (element.scrollTop = easeInOutQuad(currentTime, start, change, duration)),
      10;
    if (currentTime < duration) {
      requestAnimationFrame(animateScroll);
    } else {
      element.scrollTop = to;
    }
  };
  animateScroll();
};

export async function loadSession(id: string) {
  const client = generateClient();
  console.log('Loading session: ' + id);
  let res: any = await client.graphql({
    query: getSession,
    variables: {
      id: id ?? '',
    },
  });

  return res.data?.getSession;
}
