#ifdef XP_RELEASE
#define PUBLIC_VERSION      1 // ����ģʽ
#define GAMEMODE_4W         0 // 4wģʽ
#define PLAYER_WAIT         0 // ��ҵȴ�AI˼���������Ҫ�Ļ�
#define AI_TRAINING_SLOW    1
#define USE4W               1
#else
#define PUBLIC_VERSION      0
#define GAMEMODE_4W         0
#define PLAYER_WAIT         0
#define AI_TRAINING_SLOW    1 // ѵ��ģʽ������ʾ
#define USE4W               0
#endif
#define ATTACK_MODE         1 // �����У�0���� 1TOP 2��ƴ
#define AI_SHOW             0 // ���໥������Χ��AI
#define DISPLAY_NEXT_NUM    6 // ��ʾnext����
#if AI_TRAINING_SLOW
#define AI_TRAINING_DEEP    16
#else
#define AI_TRAINING_DEEP    6 // ѵ��AI˼�����
#endif
#define TRAINING_ROUND      20
#define AI_TRAINING_0       9
#define AI_TRAINING_2       6

#define AI_DLL_VERSION      2 // dll�汾
