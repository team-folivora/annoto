export function getUrl(path: string): string {
  let apiUrl = import.meta.env.VITE_API_URL?.toString() || "";
  return `${apiUrl}/${path}?`;
}
