import { setTimeout } from 'timers/promises';
import ora from 'ora';
import chalk from 'chalk';
import { randomInt } from 'crypto';

interface Metric {
  name: string;
  value: number | string;
  change: number;
}

async function fetchMetrics(): Promise<Metric[]> {
  const spinner = ora('Fetching latest metrics...').start();
  
  // Simulate API delay
  await setTimeout(2000);

  const metrics: Metric[] = [
    {
      name: 'Monthly Active Users (MAU)',
      value: (2.8 + randomFloat(-0.2, 0.2)).toFixed(1) + 'M',
      change: randomInt(-5, 20)
    },
    {
      name: 'Average Order Value',
      value: 24.50 + randomFloat(-2, 2),
      change: randomInt(-3, 8)  
    },
    {
      name: 'Orders per Day',
      value: 85000 + randomInt(-5000, 5000),
      change: randomInt(-5, 15)
    },
    {
      name: 'Restaurant Partners', 
      value: 3200 + randomInt(-200, 200),
      change: randomInt(-3, 10)
    },
    {
      name: 'Driver Fleet',
      value: 12500 + randomInt(-500, 500), 
      change: randomInt(-5, 12)
    }
  ];

  spinner.succeed('Metrics fetched successfully!');
  return metrics;
}

function randomFloat(min: number, max: number): number {
  return Math.random() * (max - min) + min;
}

function formatChange(change: number): string {
  const sign = change >= 0 ? '+' : '';
  return chalk[change >= 0 ? 'green' : 'red'](`${sign}${change}% MoM`);
}

async function displayMetric(metric: Metric, index: number): Promise<void> {
  // Different loading messages for variety
  const loadingMessages = [
    'Processing user data...',
    'Calculating order metrics...',
    'Analyzing daily trends...',
    'Checking partner status...',
    'Verifying fleet data...'
  ];
  
  const spinner = ora(loadingMessages[index] || 'Processing metric...').start();
  
  // Random delay between 1-3 seconds
  await setTimeout(1000 + randomInt(0, 2000));
  
  spinner.succeed(`✓ ${metric.name} processed`);
  
  // Small pause before displaying the result
  await setTimeout(500);
  
  console.log(`  ${chalk.yellow(metric.name)}: ${metric.value} (${formatChange(metric.change)})`);
  
  // Pause between metrics
  await setTimeout(800);
}

async function main() {
  console.log(chalk.blue.bold('\nBurritoNow Key Metrics Dashboard\n'));
  console.log(chalk.gray('Initializing data collection...\n'));

  try {
    const metrics = await fetchMetrics();
    
    console.log(chalk.cyan.bold('Processing individual metrics:\n'));
    
    for (let i = 0; i < metrics.length; i++) {
      await displayMetric(metrics[i], i);
    }
    
    console.log(chalk.green.bold('\n✨ All metrics processed successfully!\n'));

  } catch (error) {
    console.error(chalk.red('Error fetching metrics:'), error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
