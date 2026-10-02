import { useState } from "react";

import AIOrb from "./components/AIOrb";
import Summarizer from "./components/Summarizer";
import ImageAnalyzer from "./components/ImageAnalyzer";
import ChatBot from "./components/ChatBot";

import {
  LayoutDashboard,
  FileText,
  Image,
  MessageCircle,
  Sparkles,
  Info,
  Menu,
  X
} from "lucide-react";

import "./App.css";


function App() {

  const [activePage, setActivePage] = useState("dashboard");

  const [sidebarOpen, setSidebarOpen] = useState(false);


  const changePage = (page) => {

    setActivePage(page);

    setSidebarOpen(false);

  };


  return (

    <div className="app-layout">


      {/* =========================
          SIDEBAR
      ========================= */}

      <aside
        className={
          sidebarOpen
            ? "sidebar sidebar-open"
            : "sidebar"
        }
      >

        <div className="sidebar-logo">

          <div className="logo-icon">
            <Sparkles size={22} />
          </div>

          <div>
            <h2>SIC AI</h2>
            <span>Intelligent Workspace</span>
            <br></br>
            <span>Text • Image • Chat</span>
          </div>

        </div>


        <div className="sidebar-menu">


          <button
            className={
              activePage === "dashboard"
                ? "sidebar-item active"
                : "sidebar-item"
            }
            onClick={() =>
              changePage("dashboard")
            }
          >

            <LayoutDashboard size={20} />

            <span>
              Dashboard
            </span>

          </button>


          <button
            className={
              activePage === "summarizer"
                ? "sidebar-item active"
                : "sidebar-item"
            }
            onClick={() =>
              changePage("summarizer")
            }
          >

            <FileText size={20} />

            <span>
              Text Summarizer
            </span>

          </button>


          <button
            className={
              activePage === "image"
                ? "sidebar-item active"
                : "sidebar-item"
            }
            onClick={() =>
              changePage("image")
            }
          >

            <Image size={20} />

            <span>
              Image Intelligence
            </span>

          </button>


          <button
            className={
              activePage === "chat"
                ? "sidebar-item active"
                : "sidebar-item"
            }
            onClick={() =>
              changePage("chat")
            }
          >

            <MessageCircle size={20} />

            <span>
              AI Assistant
            </span>

          </button>


          <button
            className={
              activePage === "about"
                ? "sidebar-item active"
                : "sidebar-item"
            }
            onClick={() =>
              changePage("about")
            }
          >

            <Info size={20} />

            <span>
              About
            </span>

          </button>


        </div>


        <div className="sidebar-footer">

          <span className="status-dot"></span>

          Gemini API Online

        </div>

      </aside>


      {/* =========================
          MAIN AREA
      ========================= */}

      <main className="main-content">


        {/* TOPBAR */}

        <header className="topbar">

          <button
            className="menu-button"
            onClick={() =>
              setSidebarOpen(
                !sidebarOpen
              )
            }
          >

            {
              sidebarOpen
                ? <X />
                : <Menu />
            }

          </button>


          <div>

            <h3>
              {
                activePage === "dashboard"
                  ? "Dashboard"
                  : activePage === "summarizer"
                  ? "Text Summarizer"
                  : activePage === "image"
                  ? "Image Intelligence"
                  : activePage === "chat"
                  ? "AI Assistant"
                  : "About"
              }
            </h3>

            <p>
              SIC AI Workspace
            </p>

          </div>

        </header>


        {/* PAGE CONTENT */}

        <div className="page-content">


          {/* DASHBOARD */}

          {
            activePage === "dashboard" &&
            (

              <div className="dashboard-page">


                <div className="dashboard-hero">

                  <div className="dashboard-text">

                    <div className="badge">

                      <Sparkles size={16} />

                      Powered by Google Gemini

                    </div>


                    <h1>

                      Your Intelligent

                      <span>
                        AI Workspace
                      </span>

                    </h1>


                    <p>

                      Summarize text,
                      analyze images,
                      and interact with
                      an intelligent AI
                      assistant from one
                      workspace.

                    </p>

                  </div>


                  <div className="dashboard-orb">

                    <AIOrb />

                  </div>

                </div>


                <div className="dashboard-tools">


                  <div
                    className="dashboard-card"
                    onClick={() =>
                      changePage(
                        "summarizer"
                      )
                    }
                  >

                    <FileText />

                    <h3>
                      Text Summarizer
                    </h3>

                    <p>
                      Convert long text
                      into concise summaries.
                    </p>

                    <span>
                      Open Tool →
                    </span>

                  </div>


                  <div
                    className="dashboard-card"
                    onClick={() =>
                      changePage(
                        "image"
                      )
                    }
                  >

                    <Image />

                    <h3>
                      Image Intelligence
                    </h3>

                    <p>
                      Understand and
                      explain uploaded images.
                    </p>

                    <span>
                      Open Tool →
                    </span>

                  </div>


                  <div
                    className="dashboard-card"
                    onClick={() =>
                      changePage(
                        "chat"
                      )
                    }
                  >

                    <MessageCircle />

                    <h3>
                      AI Assistant
                    </h3>

                    <p>
                      Ask questions and
                      get intelligent answers.
                    </p>

                    <span>
                      Open Tool →
                    </span>

                  </div>


                </div>

              </div>

            )
          }


          {/* SUMMARIZER */}

          {
            activePage === "summarizer" &&
            <Summarizer />
          }


          {/* IMAGE */}

          {
            activePage === "image" &&
            <ImageAnalyzer />
          }


          {/* CHAT */}

          {
            activePage === "chat" &&
            <ChatBot />
          }


          {/* ABOUT */}

          {
            activePage === "about" &&
            (

              <div className="about-page">

                <div className="about-card">

                  <Sparkles size={40} />

                  <h2>
                    SIC AI
                  </h2>

                  <p>
                    A multimodal AI workspace for text summarization,
                    image intelligence and AI-powered conversation.
                  </p>


                  <div className="tech-list">

                    <span>React</span>

                    <span>FastAPI</span>

                    <span>Gemini AI</span>

                    <span>Three.js</span>

                  </div>

                </div>

              </div>

            )
          }


        </div>

      </main>

    </div>

  );

}


export default App;