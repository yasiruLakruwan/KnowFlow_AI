import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export type ChatResponse = {
  answer: string;
  session_id: string;
};

export const sendMessage = async (
  query: string,
  sessionId: string | null
): Promise<ChatResponse> => {
  const res = await api.post<ChatResponse>("/api/chat", {
    query,
    session_id: sessionId,
  });

  return res.data;
};

