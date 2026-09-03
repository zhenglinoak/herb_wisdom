import { fetchEventSource } from '@microsoft/fetch-event-source'
import { ElMessage } from 'element-plus'

const baseURL = 'http://localhost:8000'

export const sseRequest = async ({
    url,
    method = 'POST',
    data = null,
    onMessage,
    onClose,
    onError,
    signal,
    headers = {}
}) => {
    const token = sessionStorage.getItem('token')
    const ctrl = new AbortController()
    let completed = false
    let aborted = false

    const onAbort = () => {
        aborted = true
        ctrl.abort()
    }

    if (signal) {
        signal.addEventListener('abort', () => {
            aborted = true
            ctrl.abort()
        })
    }

    try {
        await fetchEventSource(`${baseURL}${url}`, {
            method,
            headers: {
                'Content-Type': 'application/json',
                ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
                ...headers
            },
            body: data ? JSON.stringify(data) : undefined,
            signal: ctrl.signal,
            openWhenHidden: true,

            onopen(response) {
                if (response.status === 401) {
                    sessionStorage.clear()
                    ElMessage.error('登录过期，请重新登录')
                    window.location.href = '/login'
                    ctrl.abort()
                    return
                }
                if (response.status >= 400) {
                    ElMessage.error(`请求失败: ${response.status}`)
                    ctrl.abort()
                }
            },

            onmessage(ev) {
                try {
                    const data = JSON.parse(ev.data)
                    if (data.content === '[DONE]') {
                        completed = true
                        setTimeout(() => ctrl.abort(), 100)
                        return
                    }
                    onMessage && onMessage(data)
                } catch (e) {
                    if (ev.data === '[DONE]') {
                        completed = true
                        setTimeout(() => ctrl.abort(), 100)
                        return
                    }
                    onMessage && onMessage(ev.data)
                }
            },

            onerror(err) {
                if (err.name === 'AbortError') {
                    if (completed) {
                        onClose && onClose()
                    } else if (aborted) {
                        onError && onError(err)
                    }
                    return
                }
                console.error('SSE Error:', err)
                ElMessage.error('连接服务器失败')
                onError && onError(err)
                throw err
            },

            onclose() {
                if (completed) {
                    onClose && onClose()
                }
            }
        })
    } catch (err) {
        if (err.name !== 'AbortError') {
            console.error('SSE Error:', err)
            onError && onError(err)
        }
    }

    return { abort: onAbort, completed }
}

export const createSSEController = () => {
    const controller = new AbortController()
    return controller
}