import { useState,useEffect } from "react";
import { sendMessage } from "../services/api";

export default function ChatBox(){
    const[messages,setMessages] = useState([]);
    const[input,setInput] = useState("")
    const[sessionId,setSessionId] = useState(
        localStorage.getItem("session_id")
    )
}




