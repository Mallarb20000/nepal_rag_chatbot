// In frontend/src/app/page.tsx
'use client';

import { useState } from 'react';
import ChatMessage from "./components/ChatMessage";
import ChatInputForm from "./components/ChatInputForm";

type Message = {
  role: 'user' | 'assistant';
  content: string;
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'I am an AI assistant for the Constitution of Nepal. How can I help?' }
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleUserSubmit = async (userInput: string) => {
    // Add user's message to the history
    const userMessage: Message = { role: 'user', content: userInput };
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setIsLoading(true);

    try {
      // Send message to the backend API
      const response = await fetch('https://mallarb369-nepal-rag-backend.hf.space/api/chat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userInput }),
      });

      if (!response.ok) throw new Error('Network response was not ok');

      const data = await response.json();
      
      // Add AI's response to the history
      const assistantMessage: Message = { role: 'assistant', content: data.answer };
      setMessages(prevMessages => [...prevMessages, assistantMessage]);

    } catch (error) {
      console.error("Fetch Error:", error);
      const errorMessage: Message = { role: 'assistant', content: 'Sorry, I couldn\'t connect to the server.' };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-12 bg-gray-100">
      <div className="w-full max-w-2xl flex flex-col h-[90vh]">
        <h1 className="text-4xl font-bold text-center mb-4">Nepal Constitution Chatbot</h1>
        
        <div className="flex-grow bg-white p-4 rounded-lg shadow-inner overflow-y-auto flex flex-col">
          {messages.map((msg, index) => (
            <ChatMessage key={index} role={msg.role} content={msg.content} />
          ))}
          {isLoading && <ChatMessage role="assistant" content="..." />}
        </div>
        
        <ChatInputForm onSubmit={handleUserSubmit} />
      </div>
    </main>
  );
}