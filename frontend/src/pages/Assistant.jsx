import { useState } from "react";
import { Send, Sparkles } from "lucide-react";

function Assistant() {

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([]);

  const askQuestion = () => {

    if (!question.trim()) {
      return;
    }

    const newMessage = {
      question: question,
      answer: "AI response will be connected to the backend soon."
    };

    setMessages([...messages, newMessage]);

    setQuestion("");
  };

  return (
    <div className="assistant-page">

      <div className="page-title">

        <div>
          <h1>AI Assistant</h1>

          <p>
            Ask questions about your enterprise knowledge.
          </p>
        </div>

        <div className="ai-online">
          <span></span>
          AI Online
        </div>

      </div>


      <div className="chat-container">

        <div className="chat-header">

          <div className="ai-logo">
            <Sparkles size={20} />
          </div>

          <div>
            <h2>Enterprise AI</h2>

            <p>
              Powered by your organization's knowledge base
            </p>
          </div>

        </div>


        <div className="messages">

          {messages.length === 0 && (

            <div className="empty-chat">

              <Sparkles size={35} />

              <h2>
                How can I help you?
              </h2>

              <p>
                Ask anything about your organization's documents,
                policies, reports or knowledge.
              </p>

            </div>

          )}


          {messages.map((message, index) => (

            <div key={index} className="message">

              <div className="user-question">
                <strong>You</strong>
                <p>{message.question}</p>
              </div>

              <div className="ai-answer">
                <strong>AI Assistant</strong>
                <p>{message.answer}</p>
              </div>

            </div>

          ))}

        </div>


        <div className="chat-input">

          <input
            type="text"
            value={question}
            placeholder="Ask your knowledge base..."
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                askQuestion();
              }
            }}
          />

          <button onClick={askQuestion}>
            <Send size={18} />
          </button>

        </div>

      </div>

    </div>
  );
}

export default Assistant;