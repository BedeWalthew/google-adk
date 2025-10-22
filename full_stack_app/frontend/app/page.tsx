"use client";

/**
 * Multi-Agent Chat Interface Example
 * 
 * This demonstrates how to build a frontend that works with multiple agents
 * using the Agent Registry pattern with a single /invoke endpoint.
 */

import { useState, useRef, useEffect } from "react";
import { Send, Loader2, Bot, ChevronDown } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
  agent_id?: string;
  request_id?: string;
  tokens?: number;
}

interface Agent {
  agent_id: string;
  name: string;
  model: string;
  description: string;
  metrics: {
    total_requests: number;
    successful_requests: number;
    failed_requests: number;
    total_tokens: number;
  };
}

export default function MultiAgentChat() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [agents, setAgents] = useState<Record<string, Agent>>({});
  const [selectedAgent, setSelectedAgent] = useState<string>("weather");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Fetch available agents on mount
  useEffect(() => {
    fetchAgents();
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await fetch("http://localhost:8000/agents");
      const data = await response.json();
      setAgents(data.agents);
      
      // Set first agent as default if available
      const agentIds = Object.keys(data.agents);
      if (agentIds.length > 0 && !selectedAgent) {
        setSelectedAgent(agentIds[0]);
      }
    } catch (error) {
      console.error("Failed to fetch agents:", error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading || !selectedAgent) return;

    const userMessage = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/invoke", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          agent_id: selectedAgent,
          query: userMessage,
          temperature: 0.7,
          max_tokens: 2048,
          session_id: sessionId, // Maintain conversation context
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to get response");
      }

      const data = await response.json();

      // Store session ID for conversation continuity
      if (data.session_id && !sessionId) {
        setSessionId(data.session_id);
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response,
          agent_id: data.agent_id,
          request_id: data.request_id,
          tokens: data.tokens,
        },
      ]);

      // Refresh agent metrics
      fetchAgents();
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Sorry, I encountered an error: ${
            error instanceof Error ? error.message : "Unknown error"
          }. Please try again.`,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleAgentChange = (agentId: string) => {
    setSelectedAgent(agentId);
    // Clear session when switching agents
    setSessionId(null);
    setMessages([
      {
        role: "assistant",
        content: `Switched to ${agents[agentId]?.name || agentId}. ${
          agents[agentId]?.description || ""
        }`,
      },
    ]);
  };

  const currentAgent = agents[selectedAgent];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              🤖 Multi-Agent Assistant
            </h1>
            <p className="text-gray-600">
              Enterprise-scale AI with multiple specialized agents
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            {/* Agent Selector Sidebar */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-2xl shadow-xl p-6">
                <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <Bot className="w-5 h-5" />
                  Available Agents
                </h2>

                <div className="space-y-2">
                  {Object.entries(agents).map(([agentId, agent]) => (
                    <button
                      key={agentId}
                      onClick={() => handleAgentChange(agentId)}
                      className={`w-full text-left p-3 rounded-lg transition-colors ${
                        selectedAgent === agentId
                          ? "bg-indigo-100 border-2 border-indigo-500"
                          : "bg-gray-50 hover:bg-gray-100 border-2 border-transparent"
                      }`}
                    >
                      <div className="font-medium text-sm">{agent.name}</div>
                      <div className="text-xs text-gray-500 mt-1">
                        {agent.model}
                      </div>
                      <div className="text-xs text-gray-400 mt-1">
                        {agent.metrics.total_requests} requests
                      </div>
                    </button>
                  ))}
                </div>

                {/* Current Agent Info */}
                {currentAgent && (
                  <div className="mt-6 p-3 bg-indigo-50 rounded-lg">
                    <div className="text-xs font-semibold text-indigo-900 mb-1">
                      CURRENT AGENT
                    </div>
                    <div className="text-sm text-indigo-700">
                      {currentAgent.description}
                    </div>
                    <div className="mt-2 text-xs text-indigo-600">
                      Success Rate:{" "}
                      {currentAgent.metrics.total_requests > 0
                        ? (
                            (currentAgent.metrics.successful_requests /
                              currentAgent.metrics.total_requests) *
                            100
                          ).toFixed(1)
                        : 0}
                      %
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Chat Interface */}
            <div className="lg:col-span-3">
              <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
                {/* Agent Header */}
                <div className="bg-indigo-600 text-white p-4 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Bot className="w-6 h-6" />
                    <div>
                      <div className="font-semibold">
                        {currentAgent?.name || "Select an agent"}
                      </div>
                      <div className="text-xs opacity-80">
                        {currentAgent?.model || ""}
                      </div>
                    </div>
                  </div>
                  {sessionId && (
                    <div className="text-xs opacity-80">
                      Session: {sessionId.slice(0, 8)}...
                    </div>
                  )}
                </div>

                {/* Messages */}
                <div className="h-[500px] overflow-y-auto p-6 space-y-4">
                  {messages.length === 0 && (
                    <div className="text-center text-gray-500 mt-20">
                      <Bot className="w-16 h-16 mx-auto mb-4 opacity-20" />
                      <p>Select an agent and start chatting!</p>
                    </div>
                  )}

                  {messages.map((msg, idx) => (
                    <div
                      key={idx}
                      className={`flex ${
                        msg.role === "user" ? "justify-end" : "justify-start"
                      }`}
                    >
                      <div
                        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                          msg.role === "user"
                            ? "bg-indigo-600 text-white"
                            : "bg-gray-100 text-gray-900"
                        }`}
                      >
                        {msg.agent_id && msg.role === "assistant" && (
                          <div className="text-xs opacity-70 mb-1">
                            {agents[msg.agent_id]?.name || msg.agent_id}
                          </div>
                        )}
                        <p className="text-sm whitespace-pre-wrap">
                          {msg.content}
                        </p>
                        {msg.tokens && (
                          <p className="text-xs mt-1 opacity-70">
                            {msg.tokens} tokens
                          </p>
                        )}
                      </div>
                    </div>
                  ))}

                  {isLoading && (
                    <div className="flex justify-start">
                      <div className="bg-gray-100 rounded-2xl px-4 py-3">
                        <div className="flex items-center gap-2">
                          <Loader2 className="w-4 h-4 animate-spin" />
                          <span className="text-sm text-gray-600">
                            {currentAgent?.name || "Agent"} is thinking...
                          </span>
                        </div>
                      </div>
                    </div>
                  )}

                  <div ref={messagesEndRef} />
                </div>

                {/* Input */}
                <div className="border-t p-4">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder={`Ask ${
                        currentAgent?.name || "an agent"
                      }...`}
                      disabled={isLoading || !selectedAgent}
                      className="flex-1 px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    />
                    <button
                      onClick={handleSend}
                      disabled={isLoading || !input.trim() || !selectedAgent}
                      className="px-6 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
                    >
                      <Send className="w-4 h-4" />
                      Send
                    </button>
                  </div>
                </div>
              </div>

              {/* Quick Actions */}
              <div className="mt-4 flex gap-2 flex-wrap">
                <button
                  onClick={() => {
                    setMessages([]);
                    setSessionId(null);
                  }}
                  className="px-4 py-2 bg-white rounded-lg shadow text-sm hover:bg-gray-50 transition-colors"
                >
                  Clear Chat
                </button>
                <button
                  onClick={fetchAgents}
                  className="px-4 py-2 bg-white rounded-lg shadow text-sm hover:bg-gray-50 transition-colors"
                >
                  Refresh Agents
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
