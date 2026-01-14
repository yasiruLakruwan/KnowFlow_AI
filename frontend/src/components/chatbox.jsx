import { useState,useEffect } from "react";
import { sendMessage } from "../services/api";

export default function ChatBox(){
    const[messages,setMessages] = useState([]);
    const[input,setInput] = useState("")
    const[sessionId,setSessionId] = useState(
        localStorage.getItem("session_id")
    )
}

const handleSend = async () =>{
    if (!input) return;

    setMessages([...messages, {role:"user",text:input}]);

    const response = await sendMessage(input,sessionId);

    setMessages(prev=>[
        ...prev,
        {role:"assistant",text:response.answer}
    ]);

    setInput("");
};

return (
    <div className="p-4 max-w-3xl mx-auto">
      <div className="h-96 overflow-y-auto border rounded p-3 mb-4">
        {messages.map((m, i) => (
          <div key={i} className={`mb-2 ${m.role === "user" ? "text-right" : ""}`}>
            <span className="inline-block bg-gray-200 p-2 rounded">
              {m.text}
            </span>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          className="flex-1 border rounded p-2"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Ask something..."
        />
        <button onClick={handleSend} className="bg-black text-white px-4 rounded">
          Send
        </button>
      </div>
    </div>
  );
