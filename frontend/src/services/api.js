import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000"
});

export const sendMessage = async(query,sessionId) =>{
    const res = await api.post("/chat",{
        query,
        session_id:sessionId
    });
    return res.data;
};
