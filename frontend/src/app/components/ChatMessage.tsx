// In frontend/src/components/ChatMessage.tsx

type ChatMessageProps = {
  role: 'user' | 'assistant';
  content: string;
};

export default function ChatMessage({ role, content }: ChatMessageProps) {
  const isUser = role === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} my-2`}>
      <div
        className={`max-w-md p-3 rounded-lg ${
          isUser ? 'bg-blue-500 text-white' : 'bg-gray-200 text-black'
        }`}
      >
        <p>{content}</p>
      </div>
    </div>
  );
}