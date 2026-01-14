import ChatBox from "./components/ChatBox";

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <h1 className="text-2xl font-bold text-center p-4">
        RAG Chat Application
      </h1>
      <ChatBox />
    </div>
  );
}

export default App;
