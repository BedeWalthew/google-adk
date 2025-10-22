"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <CopilotKit runtimeUrl="/api/copilotkit" agent="weather_assistant">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto">
            {/* Header */}
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-gray-900 mb-2">
                🌤️ Weather Assistant
              </h1>
              <p className="text-gray-600">
                Powered by Google ADK & CopilotKit
              </p>
            </div>

            {/* CopilotKit Chat */}
            <div className="bg-white rounded-2xl shadow-xl p-6">
              <CopilotChat
                labels={{
                  title: "Weather Assistant",
                  initial: "Hello! I'm your weather assistant. Ask me about the weather in any city!",
                }}
              />
            </div>

            {/* Info */}
            <div className="mt-6 text-center text-sm text-gray-500">
              <p>Try asking: "What's the weather in Paris?" or "Will it rain in London tomorrow?"</p>
            </div>
          </div>
        </div>
      </CopilotKit>
    </div>
  );
}
