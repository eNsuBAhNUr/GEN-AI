document.getElementById("queryForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const question = document.getElementById("question").value;
  const sqlBox = document.getElementById("sqlBox");
  const resultBox = document.getElementById("resultBox");

  const response = await fetch("http://localhost:8000/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ question })  // removed 'plot' field
  });

  const data = await response.json();

  if (data.error) {
    sqlBox.value = "";
    resultBox.value = `Error: ${data.error}`;
  } else {
    sqlBox.value = data.sql || "N/A";
    const rows = data.result?.rows || [];
    const columns = data.result?.columns || [];

    const formatted = rows.map(row =>
      row.map((val, i) => `${columns[i]}: ${val}`).join(" | ")
    ).join("\n");

    resultBox.value = formatted || "No results found.";
  }
});
