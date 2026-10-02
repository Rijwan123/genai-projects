import { useEffect, useRef, useState } from "react";
import { sendChatMessage } from "../services/api";

import {
  Send,
  Bot,
  User,
  Sparkles,
  Trash2,
} from "lucide-react";


function ChatBot() {

  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);


  // Automatically scroll to newest message
  useEffect(() => {

    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages, loading]);


  const handleSend = async () => {

    const cleanMessage = message.trim();

    if (!cleanMessage || loading) {
      return;
    }


    const userMessage = {
      role: "user",
      text: cleanMessage,
    };


    setMessages((previous) => [
      ...previous,
      userMessage,
    ]);


    setMessage("");

    setLoading(true);


    try {

      const data =
        await sendChatMessage(cleanMessage);


      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text: data.response,
        },
      ]);

    }
    catch (error) {

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text:
            "Sorry, I couldn't process your request. " +
            error.message,
        },
      ]);

    }
    finally {

      setLoading(false);

    }

  };


  const handleKeyDown = (event) => {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      handleSend();

    }

  };


  const clearChat = () => {

    setMessages([]);

    setMessage("");

  };


  return (

    <div className="qa-chat-page">


      {/* HEADER */}

      <div className="qa-chat-header">

        <div className="qa-chat-header-left">

          <div className="qa-chat-logo">
            <Bot size={25} />
          </div>

          <div>

            <h2>
              Chat with Gemini
            </h2>

            <p>
              Your AI assistant for QA,
              software testing and technology.
            </p>

          </div>

        </div>


        {messages.length > 0 && (

          <button
            className="qa-chat-clear"
            onClick={clearChat}
          >

            <Trash2 size={16} />

            Clear Chat

          </button>

        )}

      </div>


      {/* CHAT WINDOW */}

      <div className="qa-chat-window">


        {/* EMPTY STATE */}

        {messages.length === 0 && (

          <div className="qa-chat-welcome">

            <div className="qa-chat-welcome-icon">

              <Sparkles size={32} />

            </div>


            <h3>
              How can I help you today?
            </h3>


            <p>
              Hi! How can I assist you today?
            </p>


            <div className="qa-chat-suggestions">

              <button
                onClick={() =>
                  setMessage(
                    "Explain artificial intelligence in simple terms."
                  )
                }
              >
                Explain AI simply
              </button>


              <button
                onClick={() =>
                  setMessage(
                    "Help me write a professional email."
                  )
                }
              >
                Write an email
              </button>


              <button
                onClick={() =>
                  setMessage(
                    "Give me ideas for a small GenAI projects"
                  )
                }
              >
                GenAI project ideas
              </button>

            </div>

          </div>

        )}


        {/* MESSAGES */}

        {messages.map(
          (item, index) => (

            <div
              key={index}
              className={
                item.role === "user"
                  ? "qa-chat-row qa-chat-user"
                  : "qa-chat-row qa-chat-assistant"
              }
            >

              <div className="qa-chat-avatar">

                {
                  item.role === "user"
                    ? <User size={19} />
                    : <Bot size={19} />
                }

              </div>


              <div className="qa-chat-message">

                {item.text}

              </div>

            </div>

          )
        )}


        {/* TYPING */}

        {loading && (

          <div className="qa-chat-row qa-chat-assistant">

            <div className="qa-chat-avatar">

              <Bot size={19} />

            </div>


            <div className="qa-chat-message">

              <div className="qa-chat-typing">

                <span></span>
                <span></span>
                <span></span>

              </div>

            </div>

          </div>

        )}


        <div ref={messagesEndRef}></div>

      </div>


      {/* INPUT */}

      <div className="qa-chat-input-wrapper">

        <textarea
          value={message}
          onChange={(event) =>
            setMessage(event.target.value)
          }
          onKeyDown={handleKeyDown}
          placeholder="Ask your AI assistant..."
          rows={1}
        />


        <button
          className="qa-chat-send"
          onClick={handleSend}
          disabled={
            !message.trim() ||
            loading
          }
        >

          <Send size={20} />

        </button>

      </div>


      <div className="qa-chat-hint">

        Press Enter to send · Shift + Enter for a new line

      </div>

    </div>

  );

}


export default ChatBot;