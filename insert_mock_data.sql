-- IA 模拟数据插入脚本
-- 生成时间: 2025-12-30 18:56:45
-- 使用数据库
USE IA;

-- 插入用户数据（包含默认用户）
INSERT INTO users (id, username, email, password_hash, role, avatar) VALUES
(1, 'superadmin', 'superadmin@aicove.com', 'scrypt:32768:8:1$NJOYtrzJA2J55sxC$7128c09d80ac7660d992d7d1dfc5d26d3a77e5f58d95f9134a7c611d79d95d0d4503b7553bc709a494e0f72d28d904864405cbbcaef5df545f874dd1743818a1', 'super_admin', 'default.jpg'),
(2, 'admin', 'admin@aicove.com', 'scrypt:32768:8:1$x3Fv8FQD3VWN5lBm$5775f685f2087b750244e0f6b3721f51d31fd29e0de56df2531b043c1816c79e89475150a6d3e739c52a4f51123ecf4d2431cb660929bc4a1ec0a2a37fa7a790', 'admin', 'default.jpg'),
(3, 'user', 'user@aicove.com', 'scrypt:32768:8:1$xHgyNoXFECt5QwcN$f03601a5c0502fad2ef2df6ca9d445ab960691aa5d63800b7883077d450df5ef6a28208be821ca70913cf1635078b1322eab7ed8341971b474c315bb2f5ed36a', 'user', 'default.jpg'),
(4, 'testuser', 'test@aicove.com', 'scrypt:32768:8:1$nxPQ5GdC3hN2WhJb$714e7d802abe11dff571a6e56395e11451dbab5d39c1d6c78be760d9593ba3c1a72f39fa143cf8bba9652a04413029b90df4c0282dbafe0655e5910f912e62d6', 'user', 'default.jpg');

-- 插入文章数据
-- 注意：created_at和updated_at字段使用DEFAULT CURRENT_TIMESTAMP，无需手动指定
INSERT INTO articles (id, title, content, url, category, cover_image, views, likes, author_id, is_featured) VALUES
(1, '什么是大语言模型（LLM）？', '大语言模型（Large Language Model, LLM）是一种基于深度学习的自然语言处理模型，能够理解和生成人类语言。它们通过在海量文本数据上训练，学习语言的统计规律和语义关系。', NULL, '热门科普', NULL, 150, 25, 2, 1),
(2, 'ChatGPT 的工作原理', 'ChatGPT 基于 Transformer 架构，使用自注意力机制处理序列数据。它通过预训练和微调两个阶段，学习语言的生成模式，能够根据上下文生成连贯的回复。', 'https://openai.com/research/gpt-3', '热门科普', NULL, 200, 35, 2, 1),
(3, 'AI 在医疗领域的应用', '人工智能在医疗领域有着广泛的应用，包括医学影像分析、疾病诊断、药物研发等。AI 技术能够帮助医生提高诊断准确率，缩短诊断时间。', 'https://arxiv.org/list/cs.CY/recent', '最新资讯', NULL, 120, 20, 2, 0),
(4, '深度学习在图像识别中的突破', '深度学习技术，特别是卷积神经网络（CNN），在图像识别领域取得了革命性的突破。从 AlexNet 到 ResNet，再到 Vision Transformer，准确率不断提升。', 'https://arxiv.org/abs/1512.03385', '热门科普', NULL, 180, 30, 2, 1),
(5, 'AI 最新研究进展', '近期 AI 研究领域出现了多项重要进展，包括多模态大模型、强化学习新算法等。这些进展为 AI 应用开辟了新的可能性。', 'https://arxiv.org/list/cs.AI/recent', '最新资讯', NULL, 90, 15, 2, 0),
(6, 'Transformer架构详解', 'Transformer架构是自然语言处理领域的革命性突破，通过自注意力机制实现了并行计算，大大提升了训练效率。本文将深入解析Transformer的工作原理。', 'https://arxiv.org/abs/1706.03762', '热门科普', NULL, 320, 58, 2, 1),
(7, 'GPT-4技术解析', 'GPT-4是OpenAI发布的最新大语言模型，在多个基准测试中表现优异。本文详细介绍了GPT-4的技术特点、能力边界和应用场景。', 'https://openai.com/research/gpt-4', '热门科普', NULL, 450, 72, 2, 1),
(8, 'AI在自动驾驶中的应用', '自动驾驶技术是AI在交通领域的重要应用，通过计算机视觉、传感器融合和决策算法，实现车辆的自主导航。', 'https://arxiv.org/list/cs.CV/recent', '最新资讯', NULL, 280, 45, 2, 0),
(9, '深度学习框架对比：PyTorch vs TensorFlow', 'PyTorch和TensorFlow是目前最流行的两个深度学习框架。本文从易用性、性能、生态系统等多个维度进行对比分析。', 'https://pytorch.org/tutorials/', '热门科普', NULL, 380, 65, 2, 1),
(10, 'AI生成内容（AIGC）的发展趋势', 'AIGC技术正在改变内容创作方式，从文本生成到图像创作，AI正在成为创意工作者的重要工具。', 'https://arxiv.org/list/cs.CL/recent', '最新资讯', NULL, 220, 38, 2, 0),
(11, '神经网络优化技巧', '介绍深度学习中常用的优化技巧，包括学习率调整、批量归一化、残差连接等方法，帮助提升模型性能。', 'https://arxiv.org/list/cs.LG/recent', '热门科普', NULL, 290, 52, 2, 1),
(12, '大模型训练的成本与挑战', '训练大语言模型需要巨大的计算资源和数据，本文分析了训练成本、技术挑战以及可能的解决方案。', 'https://arxiv.org/list/cs.CL/recent', '最新资讯', NULL, 180, 32, 2, 0),
(13, '计算机视觉中的目标检测', '目标检测是计算机视觉的核心任务之一，从R-CNN到YOLO，算法不断演进，准确率和速度持续提升。', 'https://arxiv.org/list/cs.CV/recent', '热门科普', NULL, 340, 61, 2, 1),
(14, 'AI在金融科技中的应用', 'AI技术在金融领域有广泛应用，包括风险评估、欺诈检测、智能投顾等，正在改变传统金融服务模式。', 'https://arxiv.org/list/cs.CY/recent', '最新资讯', NULL, 250, 42, 2, 0),
(15, '强化学习入门指南', '强化学习是机器学习的重要分支，通过与环境交互学习最优策略。本文介绍强化学习的基本概念和常用算法。', 'https://arxiv.org/list/cs.LG/recent', '热门科普', NULL, 270, 48, 2, 1),
(16, '多模态AI的发展与应用', '多模态AI能够同时处理文本、图像、音频等多种类型的数据，为AI应用开辟了新的可能性。', 'https://arxiv.org/list/cs.MM/recent', '最新资讯', NULL, 210, 36, 2, 0),
(17, '自然语言处理中的预训练模型', '预训练模型如BERT、GPT等通过大规模无标注数据预训练，然后在特定任务上微调，取得了显著效果。', 'https://arxiv.org/list/cs.CL/recent', '热门科普', NULL, 360, 68, 2, 1),
(18, 'AI芯片的发展现状', 'AI芯片是AI计算的基础设施，从GPU到TPU，再到专用AI芯片，硬件创新推动AI能力不断提升。', 'https://arxiv.org/list/cs.AR/recent', '最新资讯', NULL, 190, 34, 2, 0),
(19, '生成式AI的伦理问题', '生成式AI能够创作文本、图像等内容，但也带来了版权、真实性等伦理问题，需要建立相应的治理框架。', 'https://www.example.com/generative-ai-ethics', '最新资讯', NULL, 240, 41, 2, 0),
(20, 'AI模型压缩与部署', '模型压缩技术能够减小模型体积、降低计算需求，使AI模型能够在边缘设备上高效运行。', 'https://www.example.com/model-compression', '热门科普', NULL, 310, 55, 2, 1);

-- 插入工具数据
-- 注意：created_at字段使用DEFAULT CURRENT_TIMESTAMP，无需手动指定
INSERT INTO tools (id, name, description, url, category, icon, rating, rating_count) VALUES
(1, 'ChatGPT', 'OpenAI 开发的大语言模型，支持对话、写作、编程等多种任务', 'https://chat.openai.com', '大模型', '🤖', 4.8, 1000),
(2, 'Midjourney', '强大的 AI 图像生成工具，能够根据文本描述生成高质量图像', 'https://www.midjourney.com', '图像生成', '🎨', 4.7, 800),
(3, 'GitHub Copilot', 'AI 编程助手，能够根据代码上下文自动生成代码', 'https://github.com/features/copilot', '编程', '💻', 4.6, 600),
(4, 'GPT-4', 'OpenAI 最新的大语言模型，在多个任务上表现优异', 'https://openai.com', '大模型', '🧠', 4.9, 1200),
(6, 'Gemini', 'Google 开发的多模态大语言模型，支持文本、图像、视频等多种输入', 'https://deepmind.google/technologies/gemini/', '大模型', '⭐', 4.8, 1100),
(7, '通义千问', '阿里云开发的大语言模型，支持中文对话和多种任务', 'https://tongyi.aliyun.com/', '大模型', '🌟', 4.7, 900),
(8, 'Stable Diffusion', '开源的图像生成模型，可以根据文本描述生成高质量图像', 'https://stability.ai/', '图像生成', '🎨', 4.6, 1200),
(9, 'DALL-E 2', 'OpenAI开发的图像生成模型，能够根据文本描述生成创意图像', 'https://openai.com/dall-e-2', '图像生成', '🖼️', 4.8, 1500),
(10, 'Notion AI', 'AI驱动的笔记和协作工具，支持智能写作和内容生成', 'https://www.notion.so/product/ai', '写作', '📝', 4.5, 800),
(11, 'Jasper', 'AI内容创作工具，帮助营销人员快速生成高质量文案', 'https://www.jasper.ai/', '写作', '✍️', 4.4, 700),
(12, 'DeepL', 'AI翻译工具，提供高质量的机器翻译服务，支持多种语言', 'https://www.deepl.com/', '翻译', '🌐', 4.7, 2000),
(13, 'Cursor', 'AI代码编辑器，基于GPT技术提供智能代码补全和生成', 'https://cursor.sh/', '编程', '💻', 4.6, 1000),
(14, 'Codeium', '免费的AI代码补全工具，支持多种编程语言和IDE', 'https://codeium.com/', '编程', '🔧', 4.5, 900),
(15, 'Runway ML', 'AI视频编辑和生成工具，支持视频特效、背景移除等功能', 'https://runwayml.com/', '视频', '🎬', 4.6, 1100),
(16, 'Synthesia', 'AI视频生成平台，可以创建AI虚拟人物视频', 'https://www.synthesia.io/', '视频', '🎥', 4.4, 600),
(17, 'Perplexity', 'AI搜索引擎，提供基于AI的智能搜索和问答服务', 'https://www.perplexity.ai/', '搜索', '🔍', 4.7, 1300),
(18, 'Character.AI', 'AI角色对话平台，可以与各种AI角色进行对话互动', 'https://character.ai/', '对话', '💬', 4.5, 1500),
(19, 'ElevenLabs', 'AI语音合成工具，可以生成自然流畅的语音', 'https://elevenlabs.io/', '语音', '🎤', 4.6, 800),
(20, 'Whisper', 'OpenAI开发的语音识别模型，支持多语言语音转文字', 'https://openai.com/research/whisper', '语音', '🎧', 4.8, 1400);

-- 插入案例数据
-- 注意：created_at字段使用DEFAULT CURRENT_TIMESTAMP，无需手动指定
INSERT INTO cases (id, title, description, industry, image, external_link, tags) VALUES
(1, 'AI 辅助医学影像诊断', '使用深度学习技术分析医学影像，帮助医生快速准确地识别病变', 'AI+医疗', NULL, '#', '深度学习,医学影像,诊断'),
(2, '智能教育平台', '基于 AI 的个性化学习系统，根据学生特点提供定制化教学内容', 'AI+教育', NULL, 'https://www.example.com/ai-education-platform', '个性化学习,教育,AI'),
(3, 'AI 科研助手', '利用 AI 技术加速科研文献检索和分析，提高研究效率', 'AI+科研', NULL, 'https://www.example.com/ai-research-assistant', '科研,文献检索,AI'),
(4, '智能办公系统', 'AI 驱动的办公自动化系统，提升工作效率', 'AI+办公', NULL, 'https://www.example.com/ai-office-system', '办公自动化,效率,AI'),
(5, 'AI 艺术创作平台', '使用生成式AI技术创作艺术作品，支持多种艺术风格', 'AI+艺术', NULL, 'https://www.example.com/ai-art-platform', '艺术创作,生成式AI,创意'),
(6, '智能医疗诊断系统', '基于深度学习的医疗影像分析系统，辅助医生进行疾病诊断', 'AI+医疗', NULL, '#', '医疗诊断,深度学习,影像分析'),
(7, '个性化在线教育', 'AI驱动的个性化学习平台，根据学生能力调整教学内容', 'AI+教育', NULL, '#', '在线教育,个性化学习,AI'),
(8, '智能文档处理', 'AI自动识别和处理各类文档，提高办公效率', 'AI+办公', NULL, '#', '文档处理,OCR,办公自动化');

-- 插入术语数据
-- 注意：created_at字段使用DEFAULT CURRENT_TIMESTAMP，无需手动指定
INSERT INTO terms (id, term, definition, category, related_terms, examples) VALUES
(1, 'LLM', '大语言模型（Large Language Model），是一种基于深度学习的自然语言处理模型，能够理解和生成人类语言。', 'LLM', '2,3', 'ChatGPT, GPT-4, Gemini'),
(2, 'Transformer', 'Transformer 是一种基于自注意力机制的神经网络架构，广泛应用于自然语言处理任务。', 'Transformer', '1', 'BERT, GPT, T5'),
(3, '扩散模型', '扩散模型（Diffusion Model）是一种生成模型，通过逐步去噪过程生成高质量图像。', '扩散模型', NULL, 'DALL-E 2, Stable Diffusion, Midjourney'),
(4, '神经网络', '神经网络是模拟人脑神经元连接的计算模型，由多个层和节点组成。', '核心概念', '2', '多层感知机, CNN, RNN'),
(5, '深度学习', '深度学习是机器学习的一个分支，使用多层神经网络来学习数据的表示。', '核心概念', '4', '深度神经网络, 卷积神经网络'),
(6, '机器学习', '机器学习是人工智能的一个分支，通过算法让计算机从数据中学习规律，无需显式编程。', '核心概念', '5', '监督学习, 无监督学习, 强化学习'),
(7, '卷积神经网络', '卷积神经网络（CNN）是一种专门用于处理图像数据的深度学习架构，通过卷积层提取特征。', '核心概念', '4,5', 'LeNet, AlexNet, ResNet'),
(8, '强化学习', '强化学习是机器学习的一个分支，通过与环境交互来学习最优策略，常用于游戏AI和机器人控制。', '核心概念', '6', 'Q-learning, Deep Q-Network, AlphaGo'),
(9, 'BERT', 'BERT（Bidirectional Encoder Representations from Transformers）是Google开发的预训练语言模型，使用双向Transformer编码器。', 'LLM', '2', 'BERT-base, BERT-large'),
(10, 'GPT', 'GPT（Generative Pre-trained Transformer）是OpenAI开发的生成式预训练Transformer模型，采用自回归方式生成文本。', 'LLM', '2,1', 'GPT-2, GPT-3, GPT-4'),
(11, '注意力机制', '注意力机制（Attention Mechanism）允许模型在处理序列时关注不同位置的信息，是Transformer架构的核心。', 'Transformer', '2', '自注意力, 多头注意力'),
(12, '自注意力', '自注意力（Self-Attention）是注意力机制的一种，允许序列中的每个位置关注序列中的所有位置。', 'Transformer', '11,2', 'Scaled Dot-Product Attention'),
(13, 'RNN', '循环神经网络（Recurrent Neural Network）是一种处理序列数据的神经网络，具有记忆能力。', '核心概念', '4', 'LSTM, GRU'),
(14, 'LSTM', '长短期记忆网络（Long Short-Term Memory）是一种特殊的RNN，能够学习长期依赖关系。', '核心概念', '13', '双向LSTM, 堆叠LSTM'),
(15, 'GAN', '生成对抗网络（Generative Adversarial Network）由生成器和判别器组成，通过对抗训练生成数据。', '核心概念', '5', 'DCGAN, StyleGAN, CycleGAN'),
(16, 'ResNet', '残差网络（Residual Network）通过残差连接解决深层网络训练难题，是深度学习的重要突破。', '核心概念', '7,5', 'ResNet-50, ResNet-101'),
(17, '迁移学习', '迁移学习是将在一个任务上训练的模型应用到相关任务上的技术，可以显著减少训练数据需求。', '核心概念', '5,6', '预训练模型, 微调'),
(18, '预训练', '预训练是在大规模数据上训练模型，学习通用特征表示，然后可以在特定任务上微调。', '核心概念', '17,1', 'BERT预训练, GPT预训练'),
(19, '微调', '微调（Fine-tuning）是在预训练模型基础上，使用特定任务数据继续训练的过程。', '核心概念', '17,18', 'BERT微调, GPT微调'),
(20, '监督学习', '监督学习使用标注数据训练模型，学习从输入到输出的映射关系。', '核心概念', '6', '分类, 回归'),
(21, '无监督学习', '无监督学习从未标注数据中学习数据的内在结构和模式。', '核心概念', '6', '聚类, 降维'),
(22, '梯度下降', '梯度下降是优化神经网络参数的主要方法，通过沿着损失函数梯度的反方向更新参数。', '核心概念', '5', '随机梯度下降, 批量梯度下降'),
(23, '反向传播', '反向传播算法用于计算神经网络中每个参数的梯度，是训练深度网络的关键技术。', '核心概念', '22,4', '链式法则, 梯度计算'),
(24, '过拟合', '过拟合是模型在训练数据上表现很好，但在测试数据上表现较差的现象。', '核心概念', '6', '正则化,  dropout'),
(25, '正则化', '正则化是防止过拟合的技术，通过添加惩罚项来约束模型复杂度。', '核心概念', '24', 'L1正则化, L2正则化'),
(26, 'Dropout', 'Dropout是一种正则化技术，在训练时随机丢弃部分神经元，防止过拟合。', '核心概念', '24,25', '随机失活'),
(27, '激活函数', '激活函数为神经网络引入非线性，使网络能够学习复杂模式。', '核心概念', '4', 'ReLU, Sigmoid, Tanh'),
(28, 'ReLU', 'ReLU（Rectified Linear Unit）是最常用的激活函数，计算简单且能缓解梯度消失问题。', '核心概念', '27', 'Leaky ReLU, ELU'),
(29, '损失函数', '损失函数衡量模型预测与真实值之间的差异，是训练优化的目标。', '核心概念', '22', '交叉熵, 均方误差'),
(30, '交叉熵', '交叉熵是分类任务常用的损失函数，衡量预测概率分布与真实分布的差异。', '核心概念', '29', '二元交叉熵, 多类交叉熵');

-- 插入资源数据
-- 注意：created_at字段使用DEFAULT CURRENT_TIMESTAMP，无需手动指定
INSERT INTO resources (id, title, author, type, description, cover_image, url) VALUES
(1, '深度学习', 'Ian Goodfellow', '书籍', '深度学习领域的经典教材，全面介绍深度学习的基础理论和实践方法。', NULL, '#'),
(2, 'Attention Is All You Need', 'Vaswani et al.', '论文', 'Transformer 架构的原始论文，提出了自注意力机制。', NULL, '#'),
(3, '机器学习课程', 'Andrew Ng', '课程', 'Coursera 上的经典机器学习课程，适合初学者。', NULL, '#');

-- 插入伦理专题数据
-- 注意：created_at字段使用DEFAULT CURRENT_TIMESTAMP，无需手动指定
INSERT INTO ethics_topics (id, title, slug, description, background, key_issues, expert_views, likes) VALUES
(1, 'AI 安全', 'ai-safety', '探讨 AI 系统的安全性问题，包括对抗攻击、模型鲁棒性等', '随着 AI 技术的快速发展，AI 系统的安全性问题日益凸显。如何确保 AI 系统在各种情况下都能安全可靠地运行，是一个重要的研究课题。', '对抗样本攻击、模型鲁棒性、系统可靠性、安全部署', '专家认为，AI 安全需要从多个维度进行保障，包括模型设计、训练过程、部署环境等。', 45),
(2, 'AI 偏见与公平', 'ai-bias-fairness', '讨论 AI 系统中的偏见问题，以及如何实现算法公平', 'AI 系统可能从训练数据中学习到偏见，导致对某些群体的不公平对待。', '数据偏见、算法偏见、公平性评估、去偏见方法', '实现算法公平需要从数据收集、模型设计、评估指标等多个环节进行考虑。', 38),
(3, 'AI 与就业', 'ai-employment', '探讨 AI 技术对就业市场的影响', 'AI 技术的快速发展正在改变就业市场，既有创造新岗位的机会，也有替代传统岗位的风险。', '岗位替代、新岗位创造、技能转型、职业规划', '专家建议，应该积极适应 AI 时代，学习新技能，拥抱变化。', 52),
(4, '数据隐私', 'data-privacy', '讨论 AI 应用中的数据隐私保护问题', 'AI 系统需要大量数据进行训练，如何保护用户隐私是一个重要挑战。', '数据收集、数据使用、隐私保护、合规性', '需要在技术创新和隐私保护之间找到平衡。', 41),
(5, 'AI 与人类智能', 'ai-human-intelligence', '探讨 AI 与人类智能的关系，以及 AI 是否能够真正理解', '随着 AI 能力的提升，关于 AI 是否具有真正理解能力、是否能够超越人类智能的讨论日益激烈。', '理解能力、意识问题、智能本质、人机关系', '专家认为，当前 AI 虽然在某些任务上超越人类，但缺乏真正的理解和意识。', 52),
(6, 'AI 治理与监管', 'ai-governance', '讨论 AI 技术的治理框架和监管政策', '随着 AI 技术的广泛应用，如何建立有效的治理和监管机制成为重要议题。', '监管政策、治理框架、国际协调、标准制定', '需要建立多层次、多主体的 AI 治理体系，平衡创新与风险。', 38);

-- 插入论坛帖子数据
-- 注意：created_at和updated_at字段使用DEFAULT CURRENT_TIMESTAMP，无需手动指定
INSERT INTO forum_posts (id, title, content, user_id, category, views, likes) VALUES
(1, '如何开始学习 AI？', '我是一个 AI 初学者，想了解如何系统地学习人工智能。请问应该从哪里开始？', 2, '问答', 120, 15),
(2, '分享：使用 ChatGPT 提高工作效率的经验', '最近在工作中大量使用 ChatGPT，发现它确实能显著提高工作效率。分享一下我的使用经验...', 2, '分享', 200, 35),
(3, '如何选择合适的AI模型？', '在选择AI模型时，需要考虑任务类型、数据规模、计算资源等多个因素。不同的模型有不同的特点和适用场景。', 2, '问答', 85, 18),
(4, 'Transformer架构的优势是什么？', 'Transformer架构通过自注意力机制实现了并行计算，相比RNN有更好的训练效率，同时能够捕捉长距离依赖关系。', 1, '讨论', 120, 25),
(5, '推荐一些AI学习资源', '想学习AI，但不知道从哪里开始。希望有经验的朋友推荐一些好的学习资源，包括书籍、课程、论文等。', 3, '求助', 95, 22),
(6, 'AI在医疗领域的应用案例分享', '最近在研究AI在医疗领域的应用，发现了很多有趣的案例。想和大家分享一下，也希望能听到更多的案例。', 2, '分享', 150, 30),
(7, '深度学习框架选择：PyTorch还是TensorFlow？', '作为初学者，在选择深度学习框架时很纠结。PyTorch和TensorFlow各有优势，不知道应该选择哪一个。', 3, '问答', 110, 20),
(8, 'GPT-4的使用体验分享', '最近使用了GPT-4，感觉在多个任务上都有很好的表现。想和大家分享一下使用体验，也希望能交流一些使用技巧。', 2, '分享', 180, 35),
(9, '如何理解注意力机制？', '注意力机制是Transformer的核心，但理解起来有些困难。有没有通俗易懂的解释或者可视化资源？', 3, '求助', 100, 19),
(10, 'AI生成内容的版权问题讨论', '随着AIGC技术的发展，AI生成内容的版权归属成为一个热点话题。大家怎么看这个问题？', 2, '讨论', 140, 28),
(11, '推荐一些好用的AI工具', '想收集一些实用的AI工具，包括图像生成、文本处理、代码辅助等各个方面的工具。', 3, '求助', 130, 24),
(12, '神经网络反向传播算法详解', '反向传播是训练神经网络的关键算法，通过链式法则计算梯度。本文详细解释反向传播的原理和实现。', 2, '分享', 160, 32),
(13, '如何评估AI模型的性能？', '评估AI模型性能需要选择合适的指标，不同任务有不同的评估方法。想了解一下常用的评估指标和方法。', 3, '问答', 105, 21),
(14, 'AI伦理问题思考', 'AI技术的发展带来了很多伦理问题，包括偏见、隐私、就业等。我们应该如何应对这些挑战？', 2, '讨论', 170, 38),
(15, '大模型训练的技术细节', '想了解大模型训练过程中的一些技术细节，包括数据预处理、模型架构设计、训练策略等。', 3, '问答', 125, 26);
