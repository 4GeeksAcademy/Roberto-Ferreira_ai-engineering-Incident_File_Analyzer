const http = require('http');
const { URL } = require('url');

const PORT = 4100;
const records = [
  {
    id: 'rec_101',
    full_name: 'Ana Gómez',
    email: 'ana.gomez@brasaland.com',
    phone: '+573001112233',
    position: 'Executive Assistant',
    linkedin_url: 'https://linkedin.com/in/anagomez',
    cv_url: 'https://example.com/cv/ana-gomez.pdf',
    status: 'received',
    stage: 'pending',
    experience_years: 6,
    applied_at: '2026-08-15T09:30:00.000Z',
    updated_at: '2026-08-15T09:30:00.000Z',
    notes_count: 1
  },
  {
    id: 'rec_102',
    full_name: 'Luis Ramírez',
    email: 'luis.ramirez@brasaland.com',
    phone: '+573004445566',
    position: 'Executive Assistant',
    linkedin_url: 'https://linkedin.com/in/luisramirez',
    cv_url: null,
    status: 'in_progress',
    stage: 'personal_interview',
    experience_years: 4,
    applied_at: '2026-08-17T13:10:00.000Z',
    updated_at: '2026-08-18T08:20:00.000Z',
    notes_count: 2
  },
  {
    id: 'rec_103',
    full_name: 'María Vega',
    email: 'maria.vega@brasaland.com',
    phone: '+573009998877',
    position: 'Executive Assistant',
    linkedin_url: null,
    cv_url: 'https://example.com/cv/maria-vega.pdf',
    status: 'selected',
    stage: 'offer_presented',
    experience_years: 7,
    applied_at: '2026-08-14T10:00:00.000Z',
    updated_at: '2026-08-20T12:00:00.000Z',
    notes_count: 3
  }
];

const notesByRecord = {
  rec_101: [
    { id: 'note_1', record_id: 'rec_101', content: 'Initial screening completed. Strong English and calendar experience.', created_at: '2026-08-16T08:45:00.000Z' }
  ],
  rec_102: [
    { id: 'note_2', record_id: 'rec_102', content: 'Candidate requested flexibility for travel coordination.', created_at: '2026-08-18T08:15:00.000Z' },
    { id: 'note_3', record_id: 'rec_102', content: 'Interview with People Manager went well. Follow-up scheduled.', created_at: '2026-08-19T09:00:00.000Z' }
  ],
  rec_103: [
    { id: 'note_4', record_id: 'rec_103', content: 'Offer conversation completed; legal review pending.', created_at: '2026-08-20T11:30:00.000Z' },
    { id: 'note_5', record_id: 'rec_103', content: 'Reference checks requested.', created_at: '2026-08-21T10:50:00.000Z' },
    { id: 'note_6', record_id: 'rec_103', content: 'Final approval expected this week.', created_at: '2026-08-22T16:00:00.000Z' }
  ]
};

function sendJson(res, statusCode, payload) {
  res.writeHead(statusCode, {
    'Content-Type': 'application/json; charset=utf-8',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET,POST,PUT,PATCH,DELETE,OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  });
  res.end(JSON.stringify(payload));
}

function findRecordById(id) {
  return records.find((record) => record.id === id) || null;
}

function toRecordPayload(record) {
  return {
    ...record,
    notes_count: (notesByRecord[record.id] || []).length
  };
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', (chunk) => {
      raw += chunk;
    });
    req.on('end', () => {
      if (!raw) {
        resolve({});
        return;
      }

      try {
        resolve(JSON.parse(raw));
      } catch (error) {
        reject(new Error('Invalid JSON body'));
      }
    });
    req.on('error', reject);
  });
}

const server = http.createServer(async (req, res) => {
  const requestUrl = new URL(req.url, 'http://localhost');

  if (req.method === 'OPTIONS') {
    sendJson(res, 204, {});
    return;
  }

  if (requestUrl.pathname === '/') {
    sendJson(res, 200, { ok: true, message: 'Talent Pipeline API is running.' });
    return;
  }

  const pathParts = requestUrl.pathname.split('/').filter(Boolean);

  if (pathParts[0] === 'records') {
    const recordId = pathParts[1];
    const noteId = pathParts[3];

    if (req.method === 'GET' && pathParts.length === 1) {
      const payload = records.map(toRecordPayload);
      sendJson(res, 200, {
        total: payload.length,
        page: 1,
        limit: payload.length,
        data: payload
      });
      return;
    }

    if (req.method === 'POST' && pathParts.length === 1) {
      try {
        const body = await readBody(req);
        const id = `rec_${Date.now()}`;
        const created = {
          id,
          full_name: body.full_name || 'Unknown candidate',
          email: body.email || '',
          phone: body.phone || '',
          position: body.position || 'Executive Assistant',
          linkedin_url: body.linkedin_url || null,
          cv_url: body.cv_url || null,
          status: body.status || 'received',
          stage: body.stage || 'pending',
          experience_years: Number(body.experience_years || 0),
          applied_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          notes_count: 0
        };
        records.push(created);
        notesByRecord[id] = [];
        sendJson(res, 201, created);
      } catch (error) {
        sendJson(res, 400, { error: error.message || 'Invalid request body' });
      }
      return;
    }

    if (req.method === 'GET' && pathParts.length === 2 && recordId) {
      const record = findRecordById(recordId);
      if (!record) {
        sendJson(res, 404, { error: 'Record not found' });
        return;
      }

      sendJson(res, 200, toRecordPayload(record));
      return;
    }

    if ((req.method === 'PUT' || req.method === 'PATCH') && pathParts.length === 2 && recordId) {
      try {
        const body = await readBody(req);
        const record = findRecordById(recordId);
        if (!record) {
          sendJson(res, 404, { error: 'Record not found' });
          return;
        }

        const updated = {
          ...record,
          ...body,
          updated_at: new Date().toISOString()
        };

        const index = records.findIndex((item) => item.id === recordId);
        if (index >= 0) records[index] = updated;

        sendJson(res, 200, toRecordPayload(updated));
      } catch (error) {
        sendJson(res, 400, { error: error.message || 'Invalid request body' });
      }
      return;
    }

    if (req.method === 'GET' && pathParts.length === 3 && pathParts[2] === 'notes') {
      const record = findRecordById(recordId);
      if (!record) {
        sendJson(res, 404, { error: 'Record not found' });
        return;
      }

      const list = notesByRecord[recordId] || [];
      sendJson(res, 200, { data: list, meta: { total: list.length } });
      return;
    }

    if (req.method === 'POST' && pathParts.length === 3 && pathParts[2] === 'notes') {
      try {
        const body = await readBody(req);
        const record = findRecordById(recordId);
        if (!record) {
          sendJson(res, 404, { error: 'Record not found' });
          return;
        }

        const note = {
          id: `note_${Date.now()}`,
          record_id: recordId,
          content: body.content || '',
          created_at: new Date().toISOString()
        };

        if (!notesByRecord[recordId]) notesByRecord[recordId] = [];
        notesByRecord[recordId].push(note);
        const updatedRecord = { ...record, notes_count: notesByRecord[recordId].length, updated_at: new Date().toISOString() };
        const index = records.findIndex((item) => item.id === recordId);
        if (index >= 0) records[index] = updatedRecord;

        sendJson(res, 201, note);
      } catch (error) {
        sendJson(res, 400, { error: error.message || 'Invalid note body' });
      }
      return;
    }

    if (req.method === 'DELETE' && pathParts.length === 4 && pathParts[2] === 'notes') {
      const record = findRecordById(recordId);
      if (!record) {
        sendJson(res, 404, { error: 'Record not found' });
        return;
      }

      const list = notesByRecord[recordId] || [];
      const nextList = list.filter((item) => item.id !== noteId);
      notesByRecord[recordId] = nextList;

      const updatedRecord = { ...record, notes_count: nextList.length, updated_at: new Date().toISOString() };
      const index = records.findIndex((item) => item.id === recordId);
      if (index >= 0) records[index] = updatedRecord;

      sendJson(res, 200, null);
      return;
    }
  }

  sendJson(res, 404, { error: 'Route not found' });
});

server.listen(PORT, () => {
  console.log(`Talent Pipeline API running on http://localhost:${PORT}`);
});
