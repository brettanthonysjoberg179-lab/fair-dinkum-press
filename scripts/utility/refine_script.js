
        const fs = require('fs');
        const prompt = fs.readFileSync('prompt.txt', 'utf8');
        (async () => {
            const refined = await experimental_subAgent(prompt);
            console.log(refined);
        })();
        