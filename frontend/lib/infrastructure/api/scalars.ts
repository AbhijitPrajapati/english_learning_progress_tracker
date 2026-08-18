import { ApiContractError } from "./errors";

export function toDate(value: string): Date {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    throw new ApiContractError(`API returned an invalid date-time: ${value}`);
  }
  return date;
}
