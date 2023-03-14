import torch
from transformers import BertModel, AutoModel

class RobertaModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.pretrain = BertModel.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment')
        self.dropout = torch.nn.Dropout(0.1, inplace=False)
        self.classifier = torch.nn.Linear(1024, 13)
        self.criterion = torch.nn.CrossEntropyLoss()
        
    def forward(self, input_ids, attention_mask=None, labels=None, token_type_ids=None):
        rt = {'loss': None, 'cls': None}
        
        out = self.pretrain(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)['pooler_output']
        out = self.dropout(out)
        out = self.classifier(out)
        rt['cls'] = out
                
        if(labels is not None):
            rt['loss'] = self.criterion(out, labels)
        return rt
    
class DebertaModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.pretrain = AutoModel.from_pretrained('IDEA-CCNL/Erlangshen-DeBERTa-v2-320M-Chinese')
        self.transform = torch.nn.Sequential(
            torch.nn.Linear(1024, 1024),
            torch.nn.GELU(),
            torch.nn.LayerNorm(1024, eps=1e-07, elementwise_affine=True)
        )
        self.decoder = torch.nn.Linear(1024, 14)
        self.criterion = torch.nn.CrossEntropyLoss()
        
    def forward(self, input_ids, attention_mask=None, labels=None):
        rt = {'loss': None, 'cls': None}
        
        out = self.pretrain(input_ids=input_ids, attention_mask=attention_mask)['last_hidden_state']
        out = self.transform(out)
        out = self.decoder(out)
        
        select = attention_mask.reshape(-1) == 1
        # [b, lens, 14] -> [b*lens, 14]
        out = out.reshape(-1, 14)
        out = out[select]
        rt['cls'] = out
                
        if(labels is not None):
            # [b, lens] -> [b*lens]
            labels = labels.reshape(-1)
            labels = labels[select]
            rt['loss'] = self.criterion(out, labels)
        return rt