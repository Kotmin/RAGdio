function RAGSelector() {
  return (
    <div>
      <label className="block mb-2 font-semibold">RAG Model</label>
      <select className="border px-4 py-2 rounded w-full">
        <option value="default">Default (Qdrant + GPT-4)</option>
        <option value="local">Local Model (coming soon)</option>
      </select>
    </div>
  );
}
export default RAGSelector;
