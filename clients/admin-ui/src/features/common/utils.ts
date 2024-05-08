import { format } from "date-fns-tz";

export const capitalize = (text: string): string =>
  text.replace(/^\w/, (c) => c.toUpperCase());

/**
 * "Fun On A Bun" => "Fun on a bun"
 * "fun on a bun" => "Fun on a bun"
 */
export const sentenceCase = (text: string) => {
  const lower = text.toLocaleLowerCase();
  const init = lower.substring(0, 1);
  const rest = lower.substring(1);
  return `${init.toLocaleUpperCase()}${rest}`;
};

/**
 * "funOnABun" => "Fun on a bun"
 */
export const camelToSentenceCase = (text: string) => {
  const withSpaces = text.replaceAll(/([a-z])([A-Z])/g, "$1 $2");
  return sentenceCase(withSpaces);
};

export const debounce = (fn: Function, ms = 0) => {
  let timeoutId: ReturnType<typeof setTimeout>;
  // eslint-disable-next-line func-names
  return function (this: any, ...args: any[]) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), ms);
  };
};

export const formatDate = (value: string | number | Date): string =>
  format(new Date(value), "MMMM d, Y, KK:mm:ss z");

export const utf8ToB64 = (str: string): string =>
  window.btoa(unescape(encodeURIComponent(str)));

export const getFileNameFromContentDisposition = (
  contentDisposition: string | null
) => {
  const defaultName = "export";
  if (!contentDisposition) {
    return defaultName;
  }
  const match = contentDisposition.match(/filename=(.+)/);
  return match ? match[1] : defaultName;
};

/**
 * Constructs a query string from an array of values.
 *
 * @param valueList - An array of string values to be included in the query string.
 * @param queryParam - The name of the query parameter.
 * @returns A query string where each value from the array is assigned to the query parameter.
 * If the array is empty, the function returns undefined.
 *
 * @example
 * getQueryParamsFromArray(['1', '2', '3'], 'id');
 * // returns 'id=1&id=2&id=3'
 */
export const getQueryParamsFromArray = (
  valueList: string[],
  queryParam: string
) => {
  if (valueList.length > 0) {
    return `${queryParam}=${valueList.join(`&${queryParam}=`)}`;
  }
  return undefined;
};
