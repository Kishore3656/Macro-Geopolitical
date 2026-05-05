import { useEffect, useRef, useCallback } from 'react';

interface UseWebSocketOptions<T> {
  url: string;
  onMessage: (data: T) => void;
  onConnected?: () => void;
  onDisconnected?: () => void;
  onError?: (error: string) => void;
}

export function useWebSocket<T>({
  url,
  onMessage,
  onConnected,
  onDisconnected,
  onError,
}: UseWebSocketOptions<T>) {
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();
  const reconnectAttemptsRef = useRef(0);
  const mountedRef = useRef(true);
  const connectRef = useRef<() => void>(() => {});

  const calculateBackoff = useCallback((attempt: number): number => {
    const delays = [1000, 2000, 4000, 8000, 30000];
    return delays[Math.min(attempt, delays.length - 1)];
  }, []);

  const scheduleReconnect = useCallback(() => {
    if (!mountedRef.current) return;
    const delay = calculateBackoff(reconnectAttemptsRef.current);
    reconnectAttemptsRef.current += 1;
    reconnectTimeoutRef.current = setTimeout(() => {
      connectRef.current();
    }, delay);
  }, [calculateBackoff]);

  const connect = useCallback(() => {
    if (!mountedRef.current) return;

    try {
      const ws = new WebSocket(url);

      ws.onopen = () => {
        if (!mountedRef.current) return;
        wsRef.current = ws;
        reconnectAttemptsRef.current = 0;
        onConnected?.();
      };

      ws.onmessage = (event) => {
        if (!mountedRef.current) return;
        try {
          const data = JSON.parse(event.data) as T;
          onMessage(data);
        } catch (error) {
          onError?.(`Failed to parse WS message: ${error}`);
        }
      };

      ws.onerror = () => {
        if (!mountedRef.current) return;
        onError?.('WebSocket error');
      };

      ws.onclose = () => {
        if (!mountedRef.current) return;
        wsRef.current = null;
        onDisconnected?.();
        scheduleReconnect();
      };
    } catch (error) {
      onError?.(`Failed to connect: ${error}`);
      scheduleReconnect();
    }
  }, [url, onMessage, onConnected, onDisconnected, onError, scheduleReconnect]);

  connectRef.current = connect;

  useEffect(() => {
    mountedRef.current = true;
    connect();

    return () => {
      mountedRef.current = false;
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connect]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  return { disconnect };
}
