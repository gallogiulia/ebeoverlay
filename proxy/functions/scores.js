// functions/scores.js

import fetch from "node-fetch";

export async function handler(event, context) {
  try {
      const response = await fetch("https://script.google.com/macros/s/AKfycbzyWVzWFVFUwHbBe_UhD7hKkM2WmJKfHSYOwt8oJa7FTCx_-SqCbo2fwAQ9qqJ8BIFc/exec");

    const contentType = response.headers.get("content-type");

    const data = contentType.includes("application/json")
      ? await response.json()
      : await response.text(); // fallback for debugging

    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": contentType
      },
      body: typeof data === "string" ? data : JSON.stringify(data)
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: `Function error: ${error.message}`
    };
  }
}
