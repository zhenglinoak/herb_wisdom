<template>
  <div class="chat-container">
    <!-- 左侧侧边栏 -->
    <aside class="sidebar">
      <!-- 品牌标识 -->
      <div class="brand">
        <div class="brand-icon">
          <svg viewBox="0 0 32 32" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M16 4 C 10 8, 8 14, 16 28 C 24 14, 22 8, 16 4 Z" fill="rgba(123,168,127,0.15)" />
            <line x1="16" y1="8" x2="16" y2="28" stroke-width="1" />
            <path d="M16 14 Q 12 16, 10 20" stroke-width="1" />
            <path d="M16 14 Q 20 16, 22 20" stroke-width="1" />
          </svg>
        </div>
        <div class="brand-text">
          <span class="brand-name">本草智典</span>
          <span class="brand-sub">HERBAL WISDOM</span>
        </div>
      </div>

      <!-- 搜索按钮 -->
      <div class="sidebar-search-trigger" @click="openGlobalSearch">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <span>搜索对话</span>
      </div>

      <!-- 新建对话按钮 -->
      <div class="new-chat-btn">
        <button @click="handleNewChat">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          新建对话
        </button>
      </div>

      <!-- 历史记录列表 -->
      <div class="history-list">
        <div v-for="c in chatHistory" :key="c.history_id" class="history-item"
          :class="{ active: currentChatIndex === c.history_id }" @click="handleSelectChat(c)">
          <span class="chat-title">{{ c.title }}</span>
          <button class="delete-btn" @click.stop="deleteChat(c.history_id)" title="删除对话">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>
      </div>

      <!-- 用户信息区域 -->
      <div class="user-profile">
        <div class="avatar">
          <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </div>
        <div class="user-info">
          <div class="username">{{ userName || '未登录' }}</div>
          <div class="logout" @click.stop="handleLogout">退出登录</div>
        </div>
      </div>
    </aside>

    <!-- 右侧主聊天区 -->
    <main class="main-chat">
      <!-- 顶部标题栏 -->
      <header class="chat-header">
        <div class="header-accent"></div>
        <h3>{{ currentChatTitle }}</h3>
      </header>

      <!-- 对话内容区域 -->
      <div class="chat-content" ref="chatContentRef">
        <div v-if="messages.length === 0" class="empty-state">
          <div class="empty-icon">
            <svg viewBox="0 0 64 64" width="64" height="64" fill="none" stroke="currentColor" stroke-width="1.5"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M32 8 C 20 16, 16 28, 32 56 C 48 28, 44 16, 32 8 Z" fill="rgba(74,124,89,0.08)" />
              <line x1="32" y1="16" x2="32" y2="56" stroke-width="1" />
              <path d="M32 28 Q 24 32, 20 40" stroke-width="1" />
              <path d="M32 28 Q 40 32, 44 40" stroke-width="1" />
              <path d="M32 40 Q 26 42, 23 48" stroke-width="1" />
              <path d="M32 40 Q 38 42, 41 48" stroke-width="1" />
            </svg>
          </div>
          <p class="empty-title">本草智典</p>
          <p class="empty-subtitle">开启一段新的智典对话</p>
        </div>
        <div v-else class="messages-list">
          <div v-for="(msg, index) in messages" :key="index"
            :class="['message', msg.sender, { 'msg-highlight': highlightIndex === index }]" :data-index="index">
            <!-- AI头像 -->
            <div v-if="msg.sender === 'ai'" class="msg-avatar ai-avatar">
              <svg viewBox="0 0 32 32" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.5"
                stroke-linecap="round" stroke-linejoin="round">
                <path d="M16 4 C 10 8, 8 14, 16 28 C 24 14, 22 8, 16 4 Z" fill="rgba(255,255,255,0.15)" />
                <line x1="16" y1="8" x2="16" y2="28" stroke-width="1" />
                <path d="M16 14 Q 12 16, 10 20" stroke-width="1" />
                <path d="M16 14 Q 20 16, 22 20" stroke-width="1" />
              </svg>
            </div>

            <!-- 用户头像 -->
            <div v-if="msg.sender === 'user'" class="msg-avatar user-avatar">
              <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none"
                stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>

            <div class="message-bubble">
              <div v-if="msg.isLoading" class="loading-dots">
                <span></span><span></span><span></span>
              </div>
              <!-- 使用v-html渲染Markdown解析后的HTML -->
              <div v-else-if="msg.sender === 'ai'" class="markdown-content"
                v-html="renderContentWithHighlight(msg.text, true)"></div>
              <!-- 用户消息支持关键词高亮 -->
              <div v-else v-html="renderContentWithHighlight(msg.text, false)"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 用户输入区域 -->
      <div class="input-area">
        <div class="input-wrapper">
          <textarea v-model="inputText" @keydown.enter.exact.prevent="sendMessage"
            placeholder="输入消息，按 Enter 发送，Shift + Enter 换行" rows="1" ref="textareaRef"></textarea>
          <button class="send-btn" @click="sendMessage" :disabled="!inputText.trim()">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round">
              <line x1="22" y1="2" x2="11" y2="13" />
              <polygon points="22 2 15 22 11 13 2 9 22 2" />
            </svg>
          </button>
        </div>
        <div class="footer-tip">AI 生成的内容可能不准确，请核实重要信息。</div>
      </div>
    </main>

    <!-- 右侧检索文档面板 -->
    <aside v-if="showDocsPanel && (retrievedDocs.vector?.length || retrievedDocs.bm25?.length)" class="docs-panel">
      <div class="docs-panel-header">
        <div class="docs-panel-title">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
          <span>检索文档</span>
        </div>
        <div class="docs-panel-tabs">
          <button :class="{ active: activeDocsTab === 'vector' }" @click="activeDocsTab = 'vector'">
            向量检索 ({{ retrievedDocs.vector?.length || 0 }})
          </button>
          <button :class="{ active: activeDocsTab === 'bm25' }" @click="activeDocsTab = 'bm25'">
            BM25 ({{ retrievedDocs.bm25?.length || 0 }})
          </button>
        </div>
        <button class="docs-panel-close" @click="showDocsPanel = false" title="关闭面板">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <div class="docs-panel-content">
        <template v-if="activeDocsTab === 'vector' && retrievedDocs.vector?.length">
          <div v-for="(doc, idx) in retrievedDocs.vector" :key="'v-' + idx" class="doc-card">
            <div class="doc-card-header">
              <span class="doc-badge doc-badge-vector">向量</span>
              <span class="doc-drug">{{ doc.drug_name }}</span>
              <span class="doc-disease">{{ doc.disease }}</span>
            </div>
            <div class="doc-card-body">{{ doc.page_content }}</div>
            <div class="doc-card-footer">
              <span class="doc-source" v-if="doc.source">
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                  <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
                </svg>
                {{ doc.source }}
              </span>
            </div>
          </div>
        </template>

        <template v-else-if="activeDocsTab === 'bm25' && retrievedDocs.bm25?.length">
          <div v-for="(doc, idx) in retrievedDocs.bm25" :key="'b-' + idx" class="doc-card">
            <div class="doc-card-header">
              <span class="doc-badge doc-badge-bm25">BM25</span>
              <span class="doc-drug">{{ doc.drug_name }}</span>
              <span class="doc-disease">{{ doc.disease }}</span>
            </div>
            <div class="doc-card-body">{{ doc.page_content }}</div>
            <div class="doc-card-footer">
              <span class="doc-source" v-if="doc.source">
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                  <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
                </svg>
                {{ doc.source }}
              </span>
            </div>
          </div>
        </template>

        <div v-else class="docs-panel-empty">
          <svg viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="currentColor" stroke-width="1.5"
            opacity="0.4">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <p>暂无检索文档</p>
        </div>
      </div>
    </aside>

    <Teleport to="body">
      <div v-if="globalSearchOpen" class="search-modal-overlay" @click.self="closeGlobalSearch">
        <div class="search-modal" role="dialog" aria-modal="true">
          <div class="search-modal-box">
            <svg class="search-modal-icon" viewBox="0 0 24 24" width="18" height="18">
              <path fill="currentColor"
                d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" />
            </svg>
            <input ref="globalSearchInputRef" v-model="sidebarSearchKeyword" type="text" placeholder="搜索所有对话..."
              class="search-modal-input" @keydown.enter="handleSidebarSearch" @keydown.esc="closeGlobalSearch" />
            <button v-if="sidebarSearchKeyword" class="search-modal-clear" @click="clearGlobalSearch">
              <svg viewBox="0 0 24 24" width="16" height="16">
                <path fill="currentColor"
                  d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" />
              </svg>
            </button>
            <span class="search-modal-shortcut"></span>
          </div>

          <div class="search-modal-body">
            <div v-if="sidebarSearchLoading" class="search-modal-loading">
              <svg class="spinner" viewBox="0 0 24 24" width="18" height="18">
                <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3"
                  stroke-dasharray="31.4 31.4" />
              </svg>
              搜索中...
            </div>

            <template v-else-if="sidebarSearchKeyword.trim() === ''">
              <div class="search-modal-hint">输入关键词搜索所有对话内容</div>
              <div class="search-modal-recent">


              </div>
            </template>

            <template v-else-if="sidebarSearchResults.length > 0">
              <div class="modal-result-header">
                <span>{{ sidebarSearchResults.length }} 条结果</span>
              </div>
              <div v-for="(result, idx) in sidebarSearchResults.slice(0, 20)" :key="idx" class="modal-result-item"
                @click="navigateToSearchResult(result)">
                <div class="modal-result-title">{{ result.title }}</div>
                <div class="modal-result-snippet" v-html="result.snippet"></div>
              </div>
            </template>

            <div v-else-if="!sidebarSearchLoading" class="search-modal-empty">
              <svg viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="currentColor" stroke-width="1.5"
                opacity="0.4">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
              <p>未找到匹配的对话</p>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onBeforeUnmount, watch } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import request from '@/api/request';
import { sseRequest } from '@/api/sse';
import md from '@/utils/markdown';
import 'highlight.js/styles/github.css';

const router = useRouter();
const currentChatId = ref(0);
const chatHistory = ref([]);
const messages = ref([]);
const inputText = ref('');
const currentChatIndex = ref(-1);
const chatContentRef = ref(null);
const textareaRef = ref(null);
const userName = ref('');
const sseController = ref(null);
const searchKeyword = ref('');
const highlightIndex = ref(-1);
const currentChatTitle = ref('新对话');
const retrievedDocs = ref({ vector: [], bm25: [] });
const showDocsPanel = ref(true);
const activeDocsTab = ref('vector');
const isGenerating = ref(false);
const generateProgress = ref(0);
const receivedTokens = ref(0);
let progressTimer = null;

const searchResults = computed(() => {
  const keyword = searchKeyword.value.trim().toLowerCase();
  if (!keyword) return [];
  const results = [];
  messages.value.forEach((msg, index) => {
    if (msg.isLoading) return;
    const text = (msg.text || '').toLowerCase();
    if (text.includes(keyword)) {
      const rawText = msg.text;
      const kwIndex = text.indexOf(keyword);
      const start = Math.max(0, kwIndex - 30);
      const end = Math.min(rawText.length, kwIndex + keyword.length + 30);
      let snippet = (start > 0 ? '...' : '') + rawText.slice(start, end) + (end < rawText.length ? '...' : '');
      const escaped = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      snippet = snippet.replace(new RegExp(`(${escaped})`, 'gi'), '<mark class="search-highlight">$1</mark>');
      results.push({ index, snippet });
    }
  });
  return results;
});

function clearSearch() {
  searchKeyword.value = '';
  highlightIndex.value = -1;
}

function jumpToMessage(index) {
  highlightIndex.value = index;
  nextTick(() => {
    const el = chatContentRef.value?.querySelector(`[data-index="${index}"]`);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  });
  setTimeout(() => {
    highlightIndex.value = -1;
  }, 2500);
}

function renderContentWithHighlight(text, isMarkdown) {
  if (!text) return '';
  let content = text;
  if (searchKeyword.value.trim()) {
    const keyword = searchKeyword.value.trim();
    const escaped = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    content = content.replace(new RegExp(`(${escaped})`, 'gi'), '<mark class="search-highlight">$1</mark>');
  }
  if (isMarkdown) {
    return md.render(content);
  }
  return content;
}

// ========== 侧边栏全局搜索 ==========
const sidebarSearchKeyword = ref('');
const sidebarSearchResults = ref([]);
const sidebarSearchLoading = ref(false);
const historyMessagesCache = ref({}); // { history_id: [messages] }
let searchTimer = null;

const handleSidebarSearch = () => {
  if (searchTimer) clearTimeout(searchTimer);
  const keyword = sidebarSearchKeyword.value.trim();
  if (!keyword) {
    sidebarSearchResults.value = [];
    sidebarSearchLoading.value = false;
    return;
  }
  searchTimer = setTimeout(() => {
    performSidebarSearch(keyword);
  }, 300);
};

//历史记录获取
const performSidebarSearch = async (keyword) => {
  sidebarSearchLoading.value = true;
  sidebarSearchResults.value = [];
  const results = [];
  const lowerKeyword = keyword.toLowerCase();
  const escaped = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

  try {
    for (const chat of chatHistory.value) {
      let msgs = historyMessagesCache.value[chat.history_id];
      if (!msgs) {
        try {
          const res = await request.get('/history/historyContent/' + chat.history_id);
          if (res.code === 200) {
            msgs = res.data;
            historyMessagesCache.value[chat.history_id] = msgs;
          }
        } catch (e) {
          continue;
        }
      }
      if (!msgs) continue;

      for (let i = 0; i < msgs.length; i++) {
        const msg = msgs[i];
        if (msg.isLoading) continue;
        const text = (msg.text || '').toLowerCase();
        if (text.includes(lowerKeyword)) {
          const rawText = msg.text;
          const kwIndex = text.indexOf(lowerKeyword);
          const start = Math.max(0, kwIndex - 25);
          const end = Math.min(rawText.length, kwIndex + keyword.length + 25);
          let snippet = (start > 0 ? '...' : '') + rawText.slice(start, end) + (end < rawText.length ? '...' : '');
          snippet = snippet.replace(new RegExp(`(${escaped})`, 'gi'), '<mark class="search-highlight">$1</mark>');
          results.push({
            history_id: chat.history_id,
            message_index: i,
            title: chat.title,
            snippet
          });
        }
      }
    }
    sidebarSearchResults.value = results;
  } finally {
    sidebarSearchLoading.value = false;
  }
};

const navigateToSearchResult = async (result) => {
  sidebarSearchKeyword.value = '';
  sidebarSearchResults.value = [];
  closeGlobalSearch();

  const targetChat = chatHistory.value.find(c => c.history_id === result.history_id);
  if (!targetChat) return;

  if (currentChatId.value !== result.history_id) {
    handleSelectChat(targetChat);
  }

  nextTick(() => {
    setTimeout(() => {
      const el = chatContentRef.value?.querySelector(`[data-index="${result.message_index}"]`);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        highlightIndex.value = result.message_index;
        setTimeout(() => {
          highlightIndex.value = -1;
        }, 2500);
      }
    }, 300);
  });
};

// ========== 全局搜索弹窗 ==========
const globalSearchOpen = ref(false);
const globalSearchInputRef = ref(null);

const openGlobalSearch = () => {
  globalSearchOpen.value = true;
  nextTick(() => {
    globalSearchInputRef.value?.focus();
  });
};

const closeGlobalSearch = () => {
  globalSearchOpen.value = false;
  sidebarSearchKeyword.value = '';
  sidebarSearchResults.value = [];
  sidebarSearchLoading.value = false;
};

const clearGlobalSearch = () => {
  sidebarSearchKeyword.value = '';
  sidebarSearchResults.value = [];
  globalSearchInputRef.value?.focus();
};



watch(sidebarSearchKeyword, () => {
  if (!sidebarSearchKeyword.value.trim()) {
    sidebarSearchResults.value = [];
    sidebarSearchLoading.value = false;
  }
});

// 监听消息变化，自动滚动到底部 + 更新缓存
watch(messages, () => {
  scrollToBottom();
  if (currentChatId.value !== null && currentChatId.value !== undefined && currentChatId.value !== 0) {
    historyMessagesCache.value[currentChatId.value] = messages.value;
  }
}, { deep: true });

// 监听 currentChatId 变化，同步缓存
watch(currentChatId, (newId, oldId) => {
  if (newId !== null && newId !== undefined && newId !== 0 && messages.value.length > 0) {
    historyMessagesCache.value[newId] = messages.value;
  }
});

// 初始化
onMounted(() => {
  // 自动调整 textarea 高度
  adjustTextareaHeight();

  // 获取用户名
  const storedName = sessionStorage.getItem('userName');
  if (storedName) {
    userName.value = storedName;
  }

  // 刷新左侧对话
  getMenu();
});

onBeforeUnmount(() => {
  if (sseController.value) {
    sseController.value.abort();
    sseController.value = null;
  }
});




// 方法：滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (chatContentRef.value) {
      chatContentRef.value.scrollTop = chatContentRef.value.scrollHeight;
    }
  });
};

// 方法：调整输入框高度
const adjustTextareaHeight = () => {
  const textarea = textareaRef.value;
  if (textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
  }
};

// 监听输入内容变化，调整高度
watch(inputText, () => {
  adjustTextareaHeight();
});

const handleNewChat = () => {
  if (sseController.value) {
    sseController.value.abort();
    sseController.value = null;
  }
  messages.value = [];
  inputText.value = '';
  currentChatIndex.value = -1;
  currentChatTitle.value = '新对话';
  currentChatId.value = 0;
  retrievedDocs.value = { vector: [], bm25: [] };
};

function handleSelectChat(c) {
  if (currentChatId.value === c.history_id) return;
  currentChatTitle.value = c.title;
  currentChatId.value = c.history_id;
  retrievedDocs.value = { vector: [], bm25: [] };
  request.get('/history/historyContent/' + c.history_id).then(res => {
    messages.value = res.data;
    historyMessagesCache.value[c.history_id] = res.data;
  }).catch(err => {
    ElMessage.error('获取历史记录失败');
  })
}

// 删除对话
const deleteChat = (id) => {
  ElMessageBox.confirm(
    '确定要删除这条对话记录吗?',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    request.delete('/history/deleteHistory/' + id).then(res => {
      if (res.code === 200) {
        ElMessage.success('删除成功');
        delete historyMessagesCache.value[id];
        if (currentChatId.value === id) {
          handleNewChat();
        }
        getMenu();
      }
    })
  }).catch(() => { });
};

// 保存对话
function saveChat() {
  if (messages.value.length < 2) return;

  const data = {
    "user_name": userName.value,
    "parent_id": currentChatId.value,
    "question": messages.value[messages.value.length - 2].text,
    "answer": messages.value[messages.value.length - 1].text,
  }
  request.post('/chat/saveChat', data).then(res => {
    if (res.code === 200 && res.data) {
      if (currentChatId.value === 0) {
        currentChatId.value = res.data;
      }
    }
    getMenu();
  }).catch(err => {
    ElMessage.error('保存对话失败');
  })
}

const sendMessage = async () => {
  const text = inputText.value.trim();
  if (!text) return;

  messages.value.push({
    sender: 'user',
    text: text
  });

  inputText.value = '';
  adjustTextareaHeight();

  const loadingMsgIndex = messages.value.length;
  messages.value.push({
    sender: 'ai',
    text: '',
    isLoading: true
  });

  if (sseController.value) {
    sseController.value.abort();
  }

  retrievedDocs.value = { vector: [], bm25: [] };
  showDocsPanel.value = true;

  let s = '';

  const url = `/chat/chat?q=${encodeURIComponent(text)}&id=${currentChatId.value}`;

  sseController.value = await sseRequest({
    url,
    method: 'POST',
    onMessage: (data) => {
      if (data.docs || data.vector_docs || data.bm25_docs || data.retrieved_docs) {
        const vectorDocs = data.vector_docs || (data.docs && data.docs.vector) || [];
        const bm25Docs = data.bm25_docs || (data.docs && data.docs.bm25) || [];
        const allDocs = data.retrieved_docs || data.docs || [];

        if (vectorDocs.length > 0 || bm25Docs.length > 0) {
          retrievedDocs.value = {
            vector: vectorDocs.map(d => normalizeDoc(d)),
            bm25: bm25Docs.map(d => normalizeDoc(d))
          };
        } else if (Array.isArray(allDocs) && allDocs.length > 0) {
          retrievedDocs.value = {
            vector: allDocs.slice(0, 5).map(d => normalizeDoc(d)),
            bm25: []
          };
        }
        return;
      }

      const content = data.content || data;
      if (typeof content === 'string') {
        s += content;
        messages.value[loadingMsgIndex] = {
          sender: 'ai',
          text: s,
          isLoading: false
        };
        scrollToBottom();
      }
    },
    onClose: () => {
      saveChat();
    },
    onError: (err) => {
      console.error('SSE Error:', err);
      if (err?.name !== 'AbortError') {
        messages.value[loadingMsgIndex] = {
          sender: 'ai',
          text: '抱歉，连接服务器失败，请稍后再试。',
          isLoading: false
        };
      }
    }
  });
};

const normalizeDoc = (doc) => {
  if (!doc) return null;
  if (typeof doc === 'string') {
    try { doc = JSON.parse(doc); } catch (e) { return { id: '', metadata: {}, page_content: doc }; }
  }
  return {
    id: doc.id || doc.ID || '',
    drug_name: doc.metadata?.drug_name || doc.drug_name || '',
    disease: doc.metadata?.disease || doc.disease || '',
    source: doc.metadata?.source || doc.source || '',
    page_content: doc.page_content || doc.content || doc.text || ''
  };
};

const startProgressTracking = () => {
  isGenerating.value = true;
  generateProgress.value = 5;
  receivedTokens.value = 0;

  progressTimer = setInterval(() => {
    if (generateProgress.value < 90) {
      generateProgress.value += Math.random() * 2;
    }
  }, 200);
};

const updateProgressOnToken = () => {
  receivedTokens.value++;
  const baseProgress = Math.min(85, receivedTokens.value * 0.5);
  if (baseProgress > generateProgress.value) {
    generateProgress.value = baseProgress;
  }
};

const finishProgressTracking = () => {
  if (progressTimer) {
    clearInterval(progressTimer);
    progressTimer = null;
  }
  generateProgress.value = 100;
  setTimeout(() => {
    isGenerating.value = false;
    generateProgress.value = 0;
  }, 300);
};

function getMenu() {
  request.get('/history/getMenu').then(res => {
    if (res.code === 200) {
      chatHistory.value = res.data;
    } else {
      ElMessage.error(res.msg || '获取菜单失败');
    }
  }).catch(err => {
    console.error(err);
  });
}

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    request.get('/user/logout').then((res) => {
      if (res.code === 200) {
        sessionStorage.clear();
        router.push('/login');
      }
    })
  }).catch(() => { });
};
</script>

<style scoped>
.chat-container {
  display: flex;
  width: 99vw;
  height: 97vh;
  font-family: "Noto Sans SC", "Microsoft YaHei", "PingFang SC", sans-serif;
  background-color: var(--rice-paper);
  color: var(--ink-black);
  overflow: hidden;
}

/* --- 左侧侧边栏 --- */
.sidebar {
  width: 260px;
  background: var(--herbal-dark);
  background-image:
    radial-gradient(circle at 20% 80%, rgba(74, 124, 89, 0.08) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(139, 111, 71, 0.06) 0%, transparent 50%);
  color: #e8e5df;
  display: flex;
  flex-direction: column;
  padding: 16px 12px;
  flex-shrink: 0;
  transition: width 0.3s ease;
  border-right: 1px solid rgba(212, 197, 169, 0.1);
}

/* 品牌标识 */
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 4px 16px;
  border-bottom: 1px solid rgba(212, 197, 169, 0.12);
  margin-bottom: 16px;
}

.brand-icon {
  width: 40px;
  height: 40px;
  background: rgba(123, 168, 127, 0.12);
  border: 1px solid rgba(123, 168, 127, 0.25);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--herbal-green-light);
  flex-shrink: 0;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-name {
  font-family: "Noto Serif SC", "SimSun", serif;
  font-size: 17px;
  font-weight: 600;
  color: #e8e5df;
  letter-spacing: 2px;
}

.brand-sub {
  font-size: 9px;
  color: var(--herbal-green-light);
  letter-spacing: 2px;
  opacity: 0.7;
  margin-top: 2px;
}

/* 新建对话按钮 */
.new-chat-btn {
  margin-bottom: 16px;
}

.new-chat-btn button {
  width: 100%;
  padding: 11px;
  background: rgba(74, 124, 89, 0.15);
  border: 1px solid rgba(123, 168, 127, 0.3);
  color: #e8e5df;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
  font-family: inherit;
}

.new-chat-btn button:hover {
  background: rgba(74, 124, 89, 0.25);
  border-color: rgba(123, 168, 127, 0.5);
}

/* 历史记录列表 */
.history-list {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 13.5px;
  color: #c5c3bd;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  border: 1px solid transparent;
}

.history-item:hover {
  background-color: var(--herbal-dark-2);
  color: #e8e5df;
}

.history-item.active {
  background-color: rgba(74, 124, 89, 0.2);
  border-color: rgba(123, 168, 127, 0.25);
  color: #e8e5df;
}

.history-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 60%;
  background: var(--herbal-green-light);
  border-radius: 0 2px 2px 0;
}

.chat-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
  margin-right: 8px;
}

.delete-btn {
  background: transparent;
  border: none;
  color: #8a8880;
  padding: 0;
  cursor: pointer;
  opacity: 0;
  transition: all 0.2s;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.history-item:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  color: #d4716a;
  background: rgba(212, 113, 106, 0.1);
}

/* 用户信息区域 */
.user-profile {
  border-top: 1px solid rgba(212, 197, 169, 0.12);
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 10px;
  border-radius: 8px;
  transition: background 0.2s;
}

.user-profile:hover {
  background-color: var(--herbal-dark-2);
}

.avatar {
  width: 34px;
  height: 34px;
  background: var(--tea-brown);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
  color: #f5f0e8;
}

.user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.username {
  font-size: 14px;
  font-weight: 500;
  color: #e8e5df;
}

.logout {
  font-size: 12px;
  color: #a0a098;
  margin-top: 4px;
  cursor: pointer;
  padding: 2px 0;
  width: fit-content;
  transition: color 0.2s;
}

.logout:hover {
  color: #fff;
  text-decoration: underline;
}

.logout:active {
  color: var(--herbal-green-light);
}

/* --- 右侧主聊天区 --- */
.main-chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: var(--rice-paper);
  position: relative;
  min-width: 0;
}

/* 顶部标题栏 */
.chat-header {
  padding: 14px 24px;
  border-bottom: 1px solid var(--border-warm-light);
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--rice-paper-light);
  z-index: 10;
}

.header-accent {
  width: 4px;
  height: 20px;
  background: var(--herbal-green);
  border-radius: 2px;
  flex-shrink: 0;
}

.chat-header h3 {
  margin: 0;
  font-family: "Noto Serif SC", "SimSun", serif;
  font-size: 17px;
  font-weight: 600;
  color: var(--ink-black);
  letter-spacing: 1px;
}

/* 对话内容区域 */
.chat-content {
  flex: 1;
  padding: 24px 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
  scroll-behavior: smooth;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--herbal-green);
}

.empty-icon {
  margin-bottom: 20px;
  opacity: 0.6;
}

.empty-title {
  font-family: "Noto Serif SC", "SimSun", serif;
  font-size: 26px;
  font-weight: 600;
  color: var(--herbal-green);
  letter-spacing: 4px;
  margin: 0 0 8px 0;
}

.empty-subtitle {
  font-size: 14px;
  color: var(--ink-muted);
  margin: 0;
  letter-spacing: 2px;
}

/* 消息列表 */
.messages-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

.message {
  display: flex;
  gap: 12px;
  max-width: 100%;
}

.message.user {
  flex-direction: row-reverse;
}

.msg-avatar {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ai-avatar {
  background: var(--herbal-green);
  color: #fff;
  box-shadow: 0 2px 8px rgba(74, 124, 89, 0.2);
}

.user-avatar {
  background: var(--tea-brown);
  color: #fff;
  box-shadow: 0 2px 8px rgba(139, 111, 71, 0.2);
}

.message-bubble {
  padding: 12px 18px;
  border-radius: 12px;
  line-height: 1.7;
  font-size: 15px;
  position: relative;
  max-width: 80%;
  word-wrap: break-word;
}

.message.user .message-bubble {
  background: var(--herbal-green);
  color: #fff;
  border-top-right-radius: 4px;
  box-shadow: 0 2px 8px rgba(74, 124, 89, 0.15);
}

.message.ai .message-bubble {
  background: var(--rice-paper-light);
  color: var(--ink-black);
  border: 1px solid var(--border-warm-light);
  border-top-left-radius: 4px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

/* Markdown内容样式 */
.markdown-content {
  line-height: 1.6;
  word-wrap: break-word;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  margin-top: 16px;
  margin-bottom: 8px;
  font-weight: 600;
  line-height: 1.25;
}

.markdown-content h1 {
  font-size: 1.5em;
  border-bottom: 1px solid var(--border-warm-light);
  padding-bottom: 0.3em;
}

.markdown-content h2 {
  font-size: 1.3em;
  border-bottom: 1px solid var(--border-warm-light);
  padding-bottom: 0.3em;
}

.markdown-content h3 {
  font-size: 1.15em;
}

.markdown-content p {
  margin-bottom: 12px;
}

.markdown-content ul,
.markdown-content ol {
  padding-left: 2em;
  margin-bottom: 12px;
}

.markdown-content li {
  margin-bottom: 4px;
}

.markdown-content code {
  padding: 0.2em 0.4em;
  margin: 0;
  font-size: 85%;
  background-color: rgba(27, 31, 35, 0.05);
  border-radius: 3px;
  font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
}

.markdown-content pre {
  padding: 12px;
  overflow: auto;
  font-size: 13px;
  line-height: 1.45;
  background-color: #f6f8fa;
  border-radius: 6px;
  margin-bottom: 12px;
}

.markdown-content pre code {
  background-color: transparent;
  padding: 0;
  margin: 0;
  font-size: 100%;
  border-radius: 0;
}

.markdown-content blockquote {
  padding: 0 1em;
  color: var(--ink-light);
  border-left: 0.25em solid var(--border-warm);
  margin: 0 0 12px 0;
}

.markdown-content table {
  border-spacing: 0;
  border-collapse: collapse;
  margin-bottom: 12px;
  width: 100%;
}

.markdown-content table th,
.markdown-content table td {
  padding: 6px 13px;
  border: 1px solid var(--border-warm-light);
}

.markdown-content table tr {
  background-color: var(--rice-paper-light);
  border-top: 1px solid var(--border-warm-light);
}

.markdown-content table tr:nth-child(2n) {
  background-color: var(--rice-paper);
}

.markdown-content img {
  max-width: 100%;
  box-sizing: content-box;
  background-color: var(--rice-paper);
}

.markdown-content a {
  color: var(--herbal-green);
  text-decoration: none;
}

.markdown-content a:hover {
  text-decoration: underline;
}

/* Loading 动画 */
.loading-dots {
  display: flex;
  gap: 5px;
  padding: 4px 0;
}

.loading-dots span {
  width: 7px;
  height: 7px;
  background-color: var(--herbal-green-light);
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.loading-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {

  0%,
  80%,
  100% {
    transform: scale(0);
    opacity: 0.5;
  }

  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* 输入区域 */
.input-area {
  padding: 16px 20px 20px;
  background: linear-gradient(180deg, rgba(245, 240, 232, 0) 0%, var(--rice-paper) 30%);
}

.input-wrapper {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  border: 1px solid var(--border-warm);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(139, 111, 71, 0.06);
  background: var(--rice-paper-light);
  display: flex;
  align-items: flex-end;
  padding: 8px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input-wrapper:focus-within {
  border-color: var(--herbal-green);
  box-shadow: 0 0 0 3px rgba(74, 124, 89, 0.1);
}

.input-area textarea {
  width: 100%;
  border: none;
  outline: none;
  resize: none;
  padding: 8px;
  max-height: 200px;
  font-size: 15px;
  line-height: 1.5;
  color: var(--ink-black);
  background: transparent;
  font-family: inherit;
}

.input-area textarea::placeholder {
  color: var(--ink-muted);
}

.send-btn {
  background: var(--herbal-green);
  color: white;
  border: none;
  border-radius: 8px;
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
  margin-bottom: 2px;
  margin-left: 8px;
}

.send-btn:hover {
  background: var(--herbal-green-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(74, 124, 89, 0.2);
}

.send-btn:disabled {
  background: var(--border-warm);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.footer-tip {
  text-align: center;
  font-size: 12px;
  color: var(--ink-muted);
  margin-top: 10px;
}

/* 滚动条美化 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(139, 111, 71, 0.15);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(139, 111, 71, 0.3);
}

.sidebar ::-webkit-scrollbar-thumb {
  background-color: rgba(123, 168, 127, 0.2);
}

.sidebar ::-webkit-scrollbar-thumb:hover {
  background-color: rgba(123, 168, 127, 0.4);
}


:deep(.logout-confirm-box .el-message-box__status.el-icon-warning) {
  color: #E6A23C;
  /* 比如改成橙色 */
}

/* 修改标题颜色 */
:deep(.logout-confirm-box .el-message-box__title) {
  color: #303133;
  font-weight: bold;
}

/* ========== 搜索栏 ========== */
.search-bar {
  padding: 10px 24px 0;
  position: relative;
  flex-shrink: 0;
  background: var(--rice-paper);
}

.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--rice-paper-light);
  border: 1px solid var(--border-warm);
  border-radius: 20px;
  padding: 6px 14px;
  transition: all 0.2s;
  max-width: 800px;
  margin: 0 auto;
}

.search-box:focus-within {
  background: #fff;
  border-color: var(--herbal-green);
  box-shadow: 0 0 0 3px rgba(74, 124, 89, 0.1);
}

.search-icon {
  color: var(--ink-muted);
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 14px;
  padding: 4px 0;
  min-width: 0;
  color: var(--ink-black);
}

.search-input::placeholder {
  color: var(--ink-muted);
}

.search-count {
  font-size: 12px;
  color: var(--herbal-green);
  background: rgba(74, 124, 89, 0.1);
  padding: 2px 8px;
  border-radius: 10px;
  flex-shrink: 0;
}

.search-clear {
  color: var(--ink-muted);
  cursor: pointer;
  flex-shrink: 0;
  transition: color 0.2s;
}

.search-clear:hover {
  color: var(--ink-black);
}

.search-results {
  position: absolute;
  top: 100%;
  left: 24px;
  right: 24px;
  max-height: 320px;
  overflow-y: auto;
  background: #fff;
  border: 1px solid var(--border-warm-light);
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  z-index: 100;
  margin-top: 4px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.search-results::-webkit-scrollbar {
  width: 4px;
}

.search-results::-webkit-scrollbar-thumb {
  background: var(--border-warm);
  border-radius: 4px;
}

.search-result-item {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-warm-light);
  cursor: pointer;
  transition: background 0.15s;
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-item:hover {
  background: rgba(74, 124, 89, 0.05);
}

.result-role {
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 4px;
}

.result-role.user {
  color: var(--tea-brown);
}

.result-role.ai {
  color: var(--herbal-green);
}

.result-snippet {
  font-size: 13px;
  color: var(--ink-light);
  line-height: 1.5;
}

.search-empty {
  position: absolute;
  top: 100%;
  left: 24px;
  right: 24px;
  background: #fff;
  border: 1px solid var(--border-warm-light);
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: center;
  color: var(--ink-muted);
  font-size: 13px;
  z-index: 100;
  margin-top: 4px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

/* 搜索关键词高亮 */
.search-highlight {
  background: #ffe58f;
  color: #333;
  padding: 0 2px;
  border-radius: 2px;
  font-weight: 600;
}

/* 消息定位高亮动画 */
.message.msg-highlight .message-bubble {
  animation: msgHighlight 2s ease;
  box-shadow: 0 0 0 2px var(--herbal-green);
}

@keyframes msgHighlight {
  0% {
    box-shadow: 0 0 0 4px rgba(74, 124, 89, 0.5);
  }

  30% {
    box-shadow: 0 0 0 4px rgba(74, 124, 89, 0.3);
  }

  100% {
    box-shadow: 0 0 0 2px var(--herbal-green);
  }
}

/* ========== 侧边栏搜索触发按钮 ========== */
.sidebar-search-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 12px 8px;
  padding: 8px 12px;
  background: var(--rice-paper-light);
  border: 1px solid var(--border-warm);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--ink-muted);
  font-size: 12px;
  user-select: none;
}

.sidebar-search-trigger:hover {
  background: #fff;
  border-color: var(--herbal-green);
  color: var(--herbal-green);
}

.search-shortcut {
  margin-left: auto;
  font-size: 10px;
  background: var(--border-warm-light);
  color: var(--ink-muted);
  padding: 1px 5px;
  border-radius: 3px;
  font-family: monospace;
}

/* ========== 全局搜索弹窗 ========== */
.search-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 15vh;
  z-index: 9999;
  animation: overlayFadeIn 0.2s ease;
}

@keyframes overlayFadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

.search-modal {
  width: 580px;
  max-width: 92vw;
  max-height: 70vh;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.2), 0 0 0 1px rgba(0, 0, 0, 0.04);
  overflow: hidden;
  animation: modalSlideIn 0.25s ease;
  display: flex;
  flex-direction: column;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-12px) scale(0.98);
  }

  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.search-modal-box {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 18px;
  border-bottom: 1px solid var(--border-warm-light);
}

.search-modal-icon {
  color: var(--ink-muted);
  flex-shrink: 0;
}

.search-modal-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 15px;
  color: var(--ink-black);
  padding: 4px 0;
  min-width: 0;
}

.search-modal-input::placeholder {
  color: var(--ink-muted);
}

.search-modal-clear {
  background: none;
  border: none;
  color: var(--ink-muted);
  cursor: pointer;
  padding: 2px;
  display: flex;
  border-radius: 4px;
  transition: color 0.15s;
}

.search-modal-clear:hover {
  color: var(--ink-black);
  background: var(--border-warm-light);
}

.search-modal-shortcut {
  font-size: 10px;
  color: var(--ink-muted);
  background: var(--border-warm-light);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  flex-shrink: 0;
}

.search-modal-body {
  flex: 1;
  overflow-y: auto;
  min-height: 200px;
  max-height: calc(70vh - 60px);
}

.search-modal-body::-webkit-scrollbar {
  width: 6px;
}

.search-modal-body::-webkit-scrollbar-thumb {
  background: var(--border-warm);
  border-radius: 3px;
}

.search-modal-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 40px;
  color: var(--ink-muted);
  font-size: 13px;
}

.search-modal-loading .spinner {
  animation: spin 1s linear infinite;
  color: var(--herbal-green);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.search-modal-hint {
  padding: 32px 20px 12px;
  text-align: center;
  color: var(--ink-muted);
  font-size: 13px;
}

.search-modal-recent {
  padding: 4px 0 12px;
}

.modal-section-title {
  padding: 8px 20px 6px;
  font-size: 11px;
  font-weight: 600;
  color: var(--ink-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modal-recent-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  cursor: pointer;
  transition: background 0.12s;
  color: var(--ink-light);
  font-size: 13px;
}

.modal-recent-item:hover {
  background: rgba(74, 124, 89, 0.06);
  color: var(--ink-black);
}

.recent-icon {
  color: var(--herbal-green);
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.recent-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.modal-result-header {
  padding: 10px 20px 6px;
  font-size: 11px;
  font-weight: 600;
  color: var(--herbal-green);
  border-bottom: 1px solid var(--border-warm-light);
}

.modal-result-item {
  padding: 12px 20px;
  cursor: pointer;
  border-bottom: 1px solid var(--border-warm-light);
  transition: background 0.12s;
}

.modal-result-item:last-child {
  border-bottom: none;
}

.modal-result-item:hover {
  background: rgba(74, 124, 89, 0.05);
}

.modal-result-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--tea-brown);
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.modal-result-snippet {
  font-size: 12px;
  color: var(--ink-light);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  /* 添加标准属性以提高兼容性 */
  overflow: hidden;
}


.search-modal-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 50px 20px;
  color: var(--ink-muted);
  font-size: 13px;
}

/* ========== 右侧检索文档面板 ========== */
.docs-panel {
  width: 340px;
  background: var(--rice-paper-light);
  border-left: 1px solid var(--border-warm-light);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  animation: slideInRight 0.3s ease;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }

  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.docs-panel-header {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border-warm-light);
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--rice-paper);
  flex-shrink: 0;
}

.docs-panel-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: "Noto Serif SC", "SimSun", serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--ink-black);
  flex-shrink: 0;
}

.docs-panel-title svg {
  color: var(--herbal-green);
}

.docs-panel-tabs {
  display: flex;
  gap: 4px;
  flex: 1;
  justify-content: center;
}

.docs-panel-tabs button {
  padding: 4px 10px;
  border: 1px solid var(--border-warm-light);
  background: transparent;
  border-radius: 6px;
  font-size: 12px;
  color: var(--ink-muted);
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
}

.docs-panel-tabs button:hover {
  border-color: var(--herbal-green);
  color: var(--herbal-green);
}

.docs-panel-tabs button.active {
  background: var(--herbal-green);
  border-color: var(--herbal-green);
  color: #fff;
}

.docs-panel-close {
  background: transparent;
  border: none;
  color: var(--ink-muted);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  transition: all 0.2s;
}

.docs-panel-close:hover {
  background: var(--border-warm-light);
  color: var(--ink-black);
}

.docs-panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.docs-panel-content::-webkit-scrollbar {
  width: 6px;
}

.docs-panel-content::-webkit-scrollbar-thumb {
  background: rgba(139, 111, 71, 0.15);
  border-radius: 3px;
}

.docs-panel-content::-webkit-scrollbar-thumb:hover {
  background: rgba(139, 111, 71, 0.3);
}

.doc-card {
  background: #fff;
  border: 1px solid var(--border-warm-light);
  border-radius: 10px;
  padding: 12px;
  transition: all 0.2s;
}

.doc-card:hover {
  box-shadow: 0 2px 12px rgba(74, 124, 89, 0.08);
  border-color: rgba(74, 124, 89, 0.3);
}

.doc-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.doc-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  color: #fff;
}

.doc-badge-vector {
  background: var(--herbal-green);
}

.doc-badge-bm25 {
  background: var(--tea-brown);
}

.doc-drug {
  font-size: 14px;
  font-weight: 600;
  color: var(--ink-black);
}

.doc-disease {
  font-size: 12px;
  color: var(--herbal-green);
  background: rgba(74, 124, 89, 0.1);
  padding: 2px 8px;
  border-radius: 4px;
}

.doc-card-body {
  font-size: 13px;
  color: var(--ink-light);
  line-height: 1.6;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 4;
  line-clamp: 4;
  overflow: hidden;
}

.doc-card-footer {
  display: flex;
  justify-content: flex-end;
}

.doc-source {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: var(--ink-muted);
}

.doc-source svg {
  color: var(--herbal-green);
}

.docs-panel-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 40px 20px;
  color: var(--ink-muted);
  font-size: 13px;
}
</style>