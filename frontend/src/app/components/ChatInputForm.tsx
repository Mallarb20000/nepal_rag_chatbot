// In frontend/src/app/components/ChatInputForm.tsx
'use client';

import { useState } from 'react';

type ChatInputFormProps = {
  onSubmit: (inputValue: string) => void;
};

export default function ChatInputForm({ onSubmit }: ChatInputFormProps) {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;
    
    // Instead of logging, call the function passed from the parent page
    onSubmit(inputValue); 

    setInputValue('');
  };

  return (
    <form onSubmit={handleSubmit} className="mt-4 p-4 bg-white rounded-lg shadow">
      <input
        type="text"
        className="w-full p-2 border rounded-md"
        placeholder="Ask a question..."
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
      />
    </form>
  );
}