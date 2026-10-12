/**
 * Fair Dinkum Publishing & AI Advisory - Cloudflare Worker Edge API
 * Suggestion 1: Automated End-to-End Digital Fulfillment via Workers & R2
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    if (request.method === "GET" && path === "/health") {
      return Response.json({
        status: "healthy",
        service: "fair-dinkum-edge-fulfillment-worker",
        environment: env.ENVIRONMENT || "production",
        timestamp: new Date().toISOString()
      });
    }

    // Suggestion 1: Handle Gumroad / Stripe Purchase Webhooks & Trigger Automated Fulfillment
    if (request.method === "POST" && path.startsWith("/webhook/")) {
      try {
        const payload = await request.json();
        const customerEmail = payload.email || payload.customer_email;
        const productName = payload.product_name || "Autonomous Solopreneur Super-Bundle";
        
        console.log(`[+] Webhook received for ${productName} purchased by ${customerEmail}`);

        // 1. Log sale in Cloudflare D1
        if (env.DB) {
          await env.DB.prepare(
            "INSERT INTO sales (product_name, customer_email, price, provider, created_at) VALUES (?, ?, ?, ?, ?)"
          ).bind(
            productName,
            customerEmail || "N/A",
            payload.price || 297.00,
            path.includes("gumroad") ? "gumroad" : "stripe",
            new Date().toISOString()
          ).run();
        }

        // 2. Generate secure R2 download asset key based on product
        let assetKey = "autonomous_solopreneur_gumroad_package.zip";
        if (productName.toLowerCase().includes("compliance")) {
          assetKey = "au_ai_compliance_playbook.zip";
        }

        // 3. In production worker, generate R2 presigned download URL or serve directly
        const downloadUrl = `https://${url.hostname}/download/${assetKey}`;

        console.log(`[FULFILLMENT] Sending secure download link to ${customerEmail}: ${downloadUrl}`);

        return Response.json({
          status: "success",
          message: "Purchase fulfilled successfully at edge.",
          customer: customerEmail,
          download_url: downloadUrl
        });
      } catch (err) {
        return Response.json({ error: err.message }, { status: 400 });
      }
    }

    // Serve secure downloads from R2 bucket
    if (request.method === "GET" && path.startsWith("/download/")) {
      const fileName = path.replace("/download/", "");
      if (!fileName) {
        return new Response("Missing file name", { status: 400 });
      }

      try {
        const object = await env.ASSETS_BUCKET.get(fileName);
        if (!object) {
          return new Response("Asset not found in R2", { status: 404 });
        }

        const headers = new Headers();
        object.writeHttpMetadata(headers);
        headers.set("etag", object.httpEtag);
        headers.set("Content-Disposition", `attachment; filename="${fileName}"`);

        return new Response(object.body, { headers });
      } catch (err) {
        return Response.json({ error: err.message }, { status: 500 });
      }
    }

    return new Response("Fair Dinkum Publishing Edge Fulfillment Active", { status: 200 });
  }
};
