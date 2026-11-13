
export default function ResultsPage() {
  // 表示確認用のダミーデータ
  const products = [
    {
      id: 1,
      name: "電気ケトル",
      score: 2,
      matchedTags: ["朝の習慣", "お茶"],
    },
    {
      id: 2,
      name: "ティーカップセット",
      score: 1,
      matchedTags: ["お茶"],
    },
  ];

  return (
    <main style={{ padding: "32px" }}>
      <h1>おすすめギフト</h1>
      <p>回答との一致度が高い順に表示しています。</p>

      {products.map((product) => (
        <div
          key={product.id}
          style={{
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "16px",
            marginTop: "16px",
          }}
        >
          <h2>{product.name}</h2>
          <p>一致スコア：{product.score}点</p>
          <p>一致タグ：{product.matchedTags.join("、")}</p>
        </div>
      ))}
    </main>
  );
}
