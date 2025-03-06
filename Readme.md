- Check Redis Server is running or not 
  ps aux | grep redis

- Start Redis Server 
  redis-server  [This will start the Redis server, and it will begin listening on port 6379 by default.]

- Test Redis Connection:
  redis-cli  [You can also test the connection to Redis by opening another terminal and running:]
             [If Redis is running, you will get the Redis command prompt (127.0.0.1:6379>), where you can test commands. For example, to check if Redis is storing data, try:]
             [set test_key "Hello Redis!"
             get test_key]
             [If it returns Hello Redis!, Redis is working fine.]

- Check if ClickHouse is running:
  ps aux | grep clickhouse

- Start ClickHouse Server:
  clickhouse-server start  

- Test ClickHouse Connection:
  clickhouse-client  [If ClickHouse is running, it should give you a command prompt where you can execute SQL queries, such as:]
                      [SELECT * FROM system.tables LIMIT 5;]
              

- Running Redis and ClickHouse Servers Simultaneously
You should run both servers in separate terminals, as they are two separate services.

Terminal 1: Run Redis Server with the command redis-server.
Terminal 2: Run ClickHouse Server with the command clickhouse-server start.

python src/main.py --symbol1 AAPL --symbol2 MSFT --interval daily
-----------------------------

Tommorow tasks.
1- Strategies implementation
2- Stage 5 Backtesting implementation
3- AI Agents development and integration.

-------------------------------------------


