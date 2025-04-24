

"use client";

import { useState } from "react";
import { Mic, Loader } from "lucide-react";

const Chatbot = () => {
  const [isListening, setIsListening] = useState(false);
  const [chatHistory, setChatHistory] = useState<{ type: "user" | "sabi"; message: string }[]>([]);
  const [isTyping, setIsTyping] = useState(false);

  const handleCall = () => {
    const SpeechRecognition =
      typeof window !== "undefined"
        ? (window.SpeechRecognition || window.webkitSpeechRecognition)
        : null;

    if (!SpeechRecognition) {
      alert("Speech Recognition not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.continuous = false;

    setIsListening(true);
    recognition.start();

    recognition.onresult = async (event: SpeechRecognitionEvent) => {
      const transcript = event.results[0][0].transcript;
      setChatHistory((prev) => [...prev, { type: "user", message: transcript }]);

      try {
        setIsTyping(true);
        const res = await fetch("https://sabi-production.up.railway.app/voice_chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: transcript })
        });

        if (!res.ok) throw new Error("Request failed");

        const data = await res.json();
        const reply = data.response;

        setChatHistory((prev) => [...prev, { type: "sabi", message: reply }]);

        const speak = new SpeechSynthesisUtterance(reply);
        speak.onend = () => {
          console.log("Sabi finished speaking. Listening again...");
          handleCall(); 
        };

        speechSynthesis.speak(speak);
      } catch (err) {
        console.error("Error:", err);
        setChatHistory((prev) => [...prev, { type: "sabi", message: "⚠️ Something went wrong" }]);
      } finally {
        setIsTyping(false);
        setIsListening(false);
      }
    };

    recognition.onerror = () => {
      setChatHistory((prev) => [...prev, { type: "sabi", message: "⚠️ Mic error, try again" }]);
      setIsListening(false);
    };
  };

  return (
    <div className="h-screen w-screen bg-black flex flex-col items-center justify-between text-white p-4 relative">
      <div className="w-full max-w-md mt-10 mb-4">
        <h1 className="text-2xl font-bold text-center retro-font text-[#b8ff38] mb-4">🎙️ Sabi</h1>
        <div className="w-full max-w-2xl h-[60vh] bg-gray-900 p-4 rounded-lg overflow-y-auto scrollbar-hide shadow-lg flex flex-col gap-3">
          {chatHistory.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.type === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[80%] px-4 py-2 rounded-2xl text-sm shadow-md ${
                  msg.type === "user"
                    ? "bg-[#00ffa1] text-black rounded-br-none"
                    : "bg-[#333] text-white rounded-bl-none"
                }`}
              >
                {msg.message}
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="flex justify-start text-sm text-gray-400 items-center gap-2">
              <Loader className="animate-spin h-4 w-4" /> Sabi is thinking...
            </div>
          )}
        </div>
      </div>

      <button
        onClick={handleCall}
        disabled={isListening}
        className="fixed bottom-6 right-6 bg-[#00ffa1] text-black p-4 rounded-full shadow-lg hover:scale-105 transition-all duration-200"
      >
        <Mic className={`w-6 h-6 ${isListening ? "animate-pulse" : ""}`} />
      </button>
    </div>
  );
};

export default Chatbot;

// return (
//   <div className="h-screen w-screen bg-black text-white flex flex-col items-center justify-center p-4">
//     <h1 className="text-2xl mb-4 font-mono text-green-400">🎙️ Talk to Sabi</h1>

//     <button
//       className="bg-green-600 hover:bg-green-500 px-6 py-2 rounded-full text-white text-lg disabled:opacity-50 transition-all mb-6"
//       onClick={handleCall}
//       disabled={isListening}
//     >
//       {isListening ? "Listening..." : "Call Sabi"}
//     </button>

//     <div className="w-full max-w-2xl h-[60vh] bg-gray-900 p-4 rounded-lg overflow-y-auto scrollbar-hide shadow-lg">
//       <h2 className="text-lg font-semibold mb-3 text-green-300">Conversation</h2>
//       <div className="flex flex-col gap-3">
//         {chatHistory.map((msg, idx) => (
//           <div
//             key={idx}
//             className={`flex items-start ${msg.type === "user" ? "justify-end" : "justify-start"}`}
//           >
//             {msg.type === "sabi" && (
//               <div className="mr-2 mt-[2px]">
//                 <Bot size={18} className="text-green-400" />
//               </div>
//             )}
//             <div
//               className={`rounded-xl px-4 py-2 text-sm font-mono ${
//                 msg.type === "user"
//                   ? "bg-green-600 text-white"
//                   : "bg-gray-700 text-green-200"
//               } max-w-xs`}
//             >
//               {msg.message}
//             </div>
//           </div>
//         ))}
//       </div>
//     </div>
//   </div>
// );