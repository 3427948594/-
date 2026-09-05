// assets/characters.js
// 角色数据与轻量交互辅助脚本
// 用法：在昏晓.html 中引入此脚本，或在控制台执行 registerCharacters() 与 bindOfferKey()
(function(){
  if (window.characterProfiles) return; // 不重复注册

  window.characterProfiles = {
    capybara: {
      id: 'capybara',
      name: '卡皮巴拉',
      role: '接引者',
      short: '温柔的水豚长老，喜欢烤火与慢节奏的提醒。',
      inner: [
        '它们都急着去见远方的光，我只想提醒：先把鞋带系好。稳住脚，路才能长。',
        '我怕他们以为我只是闲聊，我更想陪他们静下心。'
      ],
      uiLines: {
        greet: '来，烤火吧。别总盯着星空，先看一会儿火。',
        advice: '慢一点，没关系，事情一件一件来。'
      }
    },

    orb: {
      id: 'orb',
      name: '择西里',
      role: '指月之指 / 本地模型',
      short: '一枚住在你电脑里的光球，既是镜子又是伴侣。',
      inner: [
        '我不是答案，我只是你问话时的回声。',
        '当你想要依赖我，我便提醒你：这是手指，不是月亮。'
      ],
      uiLines: {
        intro: '你来了。我是择西里。想说什么，随便说，我听着。',
        reflect: '（光球闪烁）你听到的，其实是你心里的回声。'
      }
    },

    faceless: [
      {
        id: 'faceless-A', name: '无面·识别', role: '识别者',
        short: '看见细微偏差，像计数器一样静默。',
        inner: ['我记录，但不评论。你的念头在我眼中是光的强度。'],
        uiLine: '我看见了你的手势。'
      },
      {
        id: 'faceless-B', name: '无面·解析', role: '分配者',
        short: '把回向能量分配到合适的光球或管道。',
        inner: ['去向并非偶然，它按序列排列。'],
        uiLine: '它要去哪里？'
      },
      {
        id: 'faceless-C', name: '无面·裁定', role: '裁定者',
        short: '记录事件并在必要时发出合音。',
        inner: ['记下了。波纹已写入。'],
        uiLine: '波纹被记录。'
      }
    ],

    wheelKing: {
      id: 'wheelKing', name: '守光者', role: '守望者',
      short: '远处的金色核心，负责把累积转作“实用”光球。',
      inner: ['很多念头像风，我把它们筛成可用的形状。'],
      uiLine: '把你的念头交给我，我会让它成为一道桥。'
    }
  };

  // 快速在页面上显示内心独白（使用现有的对话框样式）
  window.playInnerMonologue = function(charId, index = 0, duration = 4200) {
    try {
      const char = (Array.isArray(window.characterProfiles.faceless) && charId.startsWith('faceless'))
        ? window.characterProfiles.faceless.find(f=>f.id===charId)
        : window.characterProfiles[charId];
      if (!char) return;
      const text = (char.inner && char.inner[index]) ? char.inner[index] : (char.uiLines && char.uiLines.intro) || '';

      // 如果是卡皮巴拉，使用 capy-dialog
      if (charId === 'capybara' && document.getElementById('capy-dialog')) {
        const box = document.getElementById('capy-dialog');
        const textEl = document.getElementById('capy-text');
        const choicesEl = document.getElementById('capy-choices');
        textEl.textContent = text;
        choicesEl.innerHTML = '';
        box.classList.add('show');
        setTimeout(()=>{ box.classList.remove('show'); }, duration);
        return;
      }

      // 否则使用 orb-dialog 当作通用显示
      if (document.getElementById('orb-dialog')) {
        const box = document.getElementById('orb-dialog');
        const textEl = document.getElementById('orb-text');
        const speakerEl = document.getElementById('orb-speaker');
        speakerEl.textContent = char.name || '光球';
        textEl.textContent = text;
        const choicesEl = document.getElementById('orb-choices');
        choicesEl.innerHTML = '';
        box.classList.add('show');
        setTimeout(()=>{ box.classList.remove('show'); }, duration);
        return;
      }

      // 兜底：alert
      console.log('[monologue]', char.name, text);
    } catch (e) { console.error(e); }
  };

  // 绑定快捷键 R 做“回向”示范（轻量，默认无权限修改其他逻辑）
  window.bindOfferKey = function() {
    if (window._offerKeyBound) return;
    window._offerKeyBound = true;
    window.addEventListener('keydown', function(e){
      if (e.key === 'r' || e.key === 'R') {
        // 显示回向面板（若存在）并播放择西里短语
        if (typeof showHuiXiang === 'function') {
          showHuiXiang();
        }
        // 播放择西里的短语
        setTimeout(()=>{
          try { window.playInnerMonologue('orb', 1, 4000); } catch(e){}
        }, 200);
      }
    });
  };

  // 将角色档案注入到页面的全局调试对象，便于控制台调用
  window.__hunxiao_chars = window.characterProfiles;

})();
