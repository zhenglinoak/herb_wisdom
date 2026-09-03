<template>
  <div style="display:flex;gap:30px;padding:20px;height:90vh;box-sizing:border-box;">
    <div style="width:380px;display:flex;flex-direction:column;">
      <input v-model="keyword" placeholder="搜索历史提问" style="width:100%;padding:8px;box-sizing:border-box;"
        @input="searchHistory" />
      <div style="margin-top:12px;overflow:auto;flex:1;" v-if="filterList.length">
        <p>匹配记录（点击查看整套对话）</p>
        <div class="search-item" v-for="item in filterList" :key="item.history_id" @click="openConversation(item)">
          {{ item.question }}
        </div>
      </div>
    </div>

    <div ref="scrollBox" style="flex:1;border:1px solid #eee;padding:16px;border-radius:6px;overflow:auto;"
      v-if="conversationList.length">
      <div class="chat-row" v-for="row in conversationList" :key="row.history_id"
        :class="{ active: selectId === row.history_id }">
        <div><strong>提问：</strong>{{ row.question }}</div>
        <div style="margin-top:8px;"><strong>回答：</strong>{{ row.answer }}</div>
        <div style="margin-top:6px;color:#666;font-size:13px;">
          {{ row.create_time }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import request from '@/api/request'

const tableData = ref([])
const keyword = ref('')
const filterList = ref([])
const conversationList = ref([])
const selectId = ref(null)
const scrollBox = ref(null)

const loadHistoryData = async () => {
  try {
    const res = await request.get('/history/getMenu')
    if (res.code === 200) {
      const historyList = res.data || []
      const allRecords = []
      for (const history of historyList) {
        try {
          const contentRes = await request.get('/history/historyContent/' + history.history_id)
          if (contentRes.code === 200 && contentRes.data) {
            const messages = contentRes.data
            for (let i = 0; i < messages.length; i += 2) {
              if (messages[i]?.sender === 'user' && messages[i + 1]?.sender === 'ai') {
                allRecords.push({
                  history_id: history.history_id,
                  question: messages[i].text,
                  answer: messages[i + 1].text,
                  user_name: history.user_name || '',
                  parent_id: '0',
                  create_time: history.create_time || new Date().toLocaleString()
                })
              }
            }
          }
        } catch (e) {
          console.error('加载历史内容失败:', e)
        }
      }
      tableData.value = allRecords
    }
  } catch (e) {
    console.error('加载历史数据失败:', e)
  }
}

loadHistoryData()

const searchHistory = () => {
  const val = keyword.value.trim().toLowerCase()
  if (!val) {
    filterList.value = []
    conversationList.value = []
    selectId.value = null
    return
  }
  filterList.value = tableData.value.filter(row =>
    row.question.toLowerCase().includes(val)
  )
}

const openConversation = (clickItem) => {
  selectId.value = clickItem.history_id
  conversationList.value = tableData.value.filter(item => {
    return item.history_id === clickItem.history_id
  })
  conversationList.value.sort((a, b) => new Date(a.create_time) - new Date(b.create_time))

  nextTick(() => {
    const domList = scrollBox.value.querySelectorAll('.chat-row')
    domList.forEach(dom => {
      if (Number(dom.dataset.id) === selectId.value) {
        dom.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
    })
  })
}
</script>

<style scoped>
.search-item {
  background: #f5f5f5;
  padding: 8px 10px;
  border-radius: 4px;
  margin-bottom: 6px;
  cursor: pointer;
}

.search-item:hover {
  background: #e9e9e9;
}

.chat-row {
  padding: 12px;
  border-radius: 6px;
  background: #fafafa;
  margin-bottom: 10px;
}

.chat-row.active {
  background: #e8f4ff;
  border: 1px solid #69a7ff;
}
</style>