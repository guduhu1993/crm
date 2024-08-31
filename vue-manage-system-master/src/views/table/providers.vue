<template>
	<div>
		<TableSearch :query="query" :options="searchOpt" :search="handleSearch" />
		<div class="container">
			<TableCustom :columns="columns" :tableData="tableData" :total="page.total" :viewFunc="handleView"
				:delFunc="handleDelete" :editFunc="handleEdit" :refresh="getData" :currentPage="page.index"
				:changePage="changePage">
				<template #toolbarBtn>
					<el-button type="warning" :icon="CirclePlusFilled" @click="visible = true">新增</el-button>
				</template>
				<!-- <template #money="{ rows }">
					￥{{ rows.money }}
				</template> -->
				<!-- <template #thumb="{ rows }">
					<el-image class="table-td-thumb" :src="rows.thumb" :z-index="10" :preview-src-list="[rows.thumb]"
						preview-teleported>
					</el-image>
				</template> -->
				<template #state="{ rows }">
					<el-tag :type="rows.state ? 'success' : 'danger'">
						{{ rows.state ? '正常' : '异常' }}
					</el-tag>
				</template>
			</TableCustom>

		</div>
		<el-dialog :title="isEdit ? '编辑' : '新增'" v-model="visible" width="700px" destroy-on-close
			:close-on-click-modal="false" @close="closeDialog">
			<TableEdit :form-data="rowData" :options="options" :edit="isEdit" :update="updateData">
				<!-- <template #thumb="{ rows }">
					<img class="table-td-thumb" :src="rows.thumb"></img>
				</template> -->
			</TableEdit>
		</el-dialog>
		<el-dialog title="查看详情" v-model="visible1" width="700px" destroy-on-close>
			<TableDetail :data="viewData">
				<!-- <template #thumb="{ rows }">
					<el-image :src="rows.thumb"></el-image>
				</template> -->
			</TableDetail>
		</el-dialog>
	</div>
</template>

<script setup lang="ts" name="providers">
import { ref, reactive } from 'vue';
import { ElMessage, } from 'element-plus';
import { CirclePlusFilled } from '@element-plus/icons-vue';
import { addProvidersData, deleteProvider, fetchData, modifyProvidersData } from '@/api/index';
import TableCustom from '@/components/table-custom.vue';
import TableDetail from '@/components/table-detail.vue';
import TableSearch from '@/components/table-search.vue';
import { TableItem } from '@/types/table';
import { FormOption, FormOptionList } from '@/types/form-option';

// 查询相关
const query = reactive({
	provider_name: '',
});
const searchOpt = ref<FormOptionList[]>([
	{ type: 'input', label: '用户名：', prop: 'provider_name' }
])
const handleSearch = () => {
	changePage(1);
};

// 表格相关
let columns = ref([
	{ type: 'selection' },
	{ type: 'index', label: '序号', width: 55, align: 'center' },
	{ prop: 'id', label: 'ID' },
	{ prop: 'provider_name', label: '用户名' },
	{ prop: 'gender', label: '性别' },
	{ prop: 'phone', label: '手机号' },
	{ prop: 'email', label: '邮箱' },
	// { prop: 'id_card', label: '身份证号' },
	// { prop: 'source_id', label: '来源' },
	// { prop: 'bank_card', label: '银行卡' },
	{ prop: 'wechat_number', label: '微信号' },
	// { prop: 'social_security', label: '社保号' },
	{ prop: 'remark', label: '备注' },
	{ prop: 'operator', label: '操作', width: 250 },
])
const page = reactive({
	index: 1,
	size: 10,
	total: 200,
})
const tableData = ref<TableItem[]>([]);
const getData = async () => {
	const res = await fetchData()
	tableData.value = res.data;
};
getData();

const changePage = (val: number) => {
	page.index = val;
	getData();
};

// 新增/编辑弹窗相关
let options = ref<FormOption>({
	labelWidth: '100px',
	span: 24,
	list: [
		{ type: 'input', label: '用户名', prop: 'provider_name', required: true },
		{ type: 'input', label: '性别', prop: 'gender', required: true },
		{ type: 'input', label: '手机号', prop: 'phone', required: true },
		{ type: 'input', label: '邮箱', prop: 'email' },
		{ type: 'input', label: '微信号', prop: 'wechat_number' },
		// { type: 'input', label: '来源', prop: 'source_id', required: true},
		{ type: 'input', label: '身份证', prop: 'id_card', required: true },
		{ type: 'input', label: '社保号', prop: 'social_security', required: true },
		{ type: 'input', label: '银行卡', prop: 'bank_card', required: true },
		{ type: 'input', label: '备注', prop: 'remark'},
		// { type: 'switch', activeText: '正常', inactiveText: '异常', label: '账户状态', prop: 'state', required: true },
		// { type: 'upload', label: '头像', prop: 'thumb', required: true },
	]
})
const visible = ref(false);
const isEdit = ref(false);
const rowData = ref({});
const handleEdit = (row: TableItem) => {
	rowData.value = { ...row };
	isEdit.value = true;
	visible.value = true;
};

const changeData = async (isEdit_value, val) => {
	if (isEdit_value==true) {
		await modifyProvidersData(val)
	} else if (isEdit_value==false){
		await addProvidersData(val)
	} else {
		console.log('error')
	}
};

const updateData = async (val) => {
	await changeData(isEdit.value, val).then(() => {
		ElMessage.success('编辑成功');
		closeDialog();
		getData();
	})
	
};

const closeDialog = () => {
	visible.value = false;
	isEdit.value = false;
};

// 查看详情弹窗相关
const visible1 = ref(false);
const viewData = ref({
	row: {},
	list: []
});
const handleView = (row: TableItem) => {
	viewData.value.row = { ...row }
	viewData.value.list = [
		// {
		// 	prop: 'id',
		// 	label: '用户ID',
		// },
		{
			prop: 'social_security',
			label: '社保号',
		},
		{
			prop: 'id_card',
			label: '身份证',
		},
		{
			prop: 'bank_card',
			label: '银行卡号',
		},
		// {
		// 	prop: 'source_id',
		// 	label: '来源',
		// },
		{
			prop: 'remark',
			label: '备注',
		},
	]
	visible1.value = true;
};

// 删除相关
const handleDelete = async (row: TableItem) => {
	await deleteProvider(row.id).then(() => {
		getData();
		ElMessage.success('删除成功');
	});
}

</script>

<style scoped>
.table-td-thumb {
	display: block;
	margin: auto;
	width: 40px;
	height: 40px;
}
</style>
