const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('Running Portfolio Verification (Node.js Test Runner)...');

try {
    // Run Python verification suite
    const output = execSync('python test_portfolio.py', { encoding: 'utf-8' });
    console.log(output);
    console.log('All tests passed successfully!');
    process.exit(0);
} catch (error) {
    console.error('Test execution failed:');
    if (error.stdout) console.log(error.stdout);
    if (error.stderr) console.error(error.stderr);
    process.exit(1);
}
